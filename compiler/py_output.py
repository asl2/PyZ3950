#!/usr/bin/env python

import sys
import visitor
import compiler
import time

class Visitor:
    def __init__ (self, defined_dict, source_name, indent = 0):
        self.source_name = source_name
        self.defined_dict  = defined_dict
        self.tags_def = 'EXPLICIT' # default default tag is explicit, but can override at module level
        self.indent_lev = 0
        self.assignments = {}
        self.dependencies = {}
        self.pyquotes = []
        self.defined_dict = defined_dict
        self.name_ctr = 0
        self.text = ''
    def save (self):
        so_far = self.text
        self.text = ''
        return so_far
    def restore (self, text):
        self.text = text
    def output (self, data):
        self.text += data
    def finish (self):
        self.output_assignments ()
        self.output_pyquotes ()
        print(self.text)
    def spaces (self):
        return " " * (4 * self.indent_lev)
    def indent (self):
        self.indent_lev += 1
    def outdent (self):
        self.indent_lev -= 1
        assert (self.indent_lev >= 0)
    def register_assignment (self, ident, val, dependencies):
        if ident in self.assignments:
            raise "Duplicate assignment for " + ident
        if ident in self.defined_dict:
            raise "cross-module duplicates for " + ident
        self.defined_dict [ident] = 1
        self.assignments[ident] = val
        self.dependencies [ident] = dependencies
#        self.output ("#%s depends on %s" % (ident, str (dependencies))
    def register_pyquote (self, val):
        self.pyquotes.append (val)
    def output_assignments (self):
        # XXX topo-sorting should be in main compiler
        already_output = {}
        text_list = []
        assign_keys = list(self.assignments.keys())
        to_output_count = len (assign_keys)
        while 1:
            any_output = 0
            for (ident, val) in self.assignments.items ():
                if ident in already_output:
                    continue
                ok = 1
                for d in self.dependencies [ident]:
                    if (d not in already_output and
                        d in assign_keys):
                        ok = 0
                if ok:
                    text_list.append ("%s=%s" % (ident,
                                                self.assignments [ident]))
                    already_output [ident] = 1
                    any_output = 1
                    to_output_count -= 1
                    assert (to_output_count >= 0)
            if not any_output:
                if to_output_count == 0:
                    break
                # OK, we detected a cycle
                cycle_ident_list = []
                cycle_list = []
                for ident in self.assignments.keys ():
                    if ident not in already_output:
                        text_list.append ('%s = asn1.Promise("%s")' %
                                          (ident, ident))
                        cycle_ident_list.append (ident)
                        depend_list = [d for d in self.dependencies[ident] if d in assign_keys]
                        cycle_list.append ("%s(%s)" % (ident, ",".join (depend_list)))
                        
                text_list.append ("# Cycle XXX " + ",".join (cycle_list))
                promises_dict = {}
                for ident in cycle_ident_list:
                    text_list.append("%s=%s" % (ident,self.assignments[ident]))

                text_list.append ("_promises_dict = {")
                for ident in cycle_ident_list:
                    text_list.append ("'%s' : %s," % (ident, ident))
                text_list.append ("}")
                for ident in cycle_ident_list:
                    text_list.append ("%s.fulfill_promises (_promises_dict)"
                                      % ident)
                break

        self.output ("\n".join (text_list))
        self.output ("\n")
    def output_pyquotes (self):
        self.output ("\n".join (self.pyquotes))
        self.output ("\n")
    def make_new_name (self):
        self.name_ctr += 1
        return "_compiler_generated_name_%d" % (self.name_ctr,)
    def set_walker (self, walker):
        self.walker = walker
    def visit_saving (self, node):
        text = self.save ()
        self.walker.dispatch (node)
        s = self.text
        self.restore (text)
        return s

    def visitModule (self, node):
        self.tag_def = node.tag_def.dfl_tag # XXX or prepass to propagate def tag throughout

        # XXX handle node.imports, node.exports, node.ident.assigned_ident
        self.output ("#module %s None\n" % (node.ident.name,))
        # XXX none to handle back-compat comparing
        return node.assign_list
    def visitType_Assign (self, node):
        dep_dict = {}
        compiler.calc_dependencies (node.val, dep_dict, 0)
        depend_list = list(dep_dict.keys ())
        s = self.visit_saving (node.val)
        self.register_assignment (node.name.name, s,  depend_list)

    def visitValue_Assign (self, node):
        self.output ("#Value_assign")
    def visitPyQuote (self, node):
        self.register_pyquote (node.val)
    def handleNamedNumList (self, node):
        def mk_named_num (nn):
            return "('%s',%s)" % (nn.ident, nn.val)
        names = ",".join (map (mk_named_num, node.named_list))
        lo = None
        hi = None
        if hasattr (node, 'subtype'):
            assert (len (node.subtype) == 1) # XXX take intersection
            st = node.subtype [0]
            if isinstance (st, compiler.ValueRange):
                lo = st.lo
                hi = st.hi
            # XXX might also be size (for bitstrings)
        self.output ("asn1.%s_class ([%s],%s,%s)" % (node.asn1_typ, names,
                                                     lo, hi))
    visitInteger = handleNamedNumList
    visitBitString = handleNamedNumList

    def visitType_Ref (self, node):
        self.output (node.name)
    def mk_seq_or_set_of (name):
        def work (self, node):
            s = self.visit_saving (node.val)
            self.output ('%sasn1.%s (%s)' % (self.spaces (), name, s)) # XXX handle node.size_constr
        return work
    visitSequence_Of = mk_seq_or_set_of ('SEQUENCE_OF')
    visitSet_Of = mk_seq_or_set_of ('SET_OF')

    def visitTag (self, node):
        s = self.visit_saving (node.typ)
        val = node.tag.num
        typ = node.tag_typ.upper()
        if typ == 'DEFAULT':
            typ = self.tags_def # XXX should propagate in compiler
        tag_str =  'asn1.%s(%d,cls=asn1.%s_FLAG)' % (typ, val, node.tag.cls) 

        self.output ('asn1.TYPE(%s,%s)' % (tag_str, s))
    def visitEnum (self, node):
        def strify_one (named_num):
            return "%s=%s" % (named_num.ident, named_num.val)
        self.output ("asn1.ENUM(%s)" % ",".join (map (strify_one, node.val)))
    def visitBaseType (self, node):
        self.output ("asn1.%s" % node.val)
    def visitLiteral (self, node):
        self.output (node.val)
    def mk_seq_or_choice_str (self, node):
        self.indent ()
        def visit_list (l):
            slist = list(map (self.visit_saving, l))
            return (",\n%s"% self.spaces ()).join (slist)

        mainstr = visit_list (node.elt_list)
        if node.ext_list != None:
            extstr = visit_list (node.ext_list)
        else:
            extstr = None
        self.outdent ()
        return (mainstr, extstr)
    def visitSequence (self, node):
        seq_name = getattr (node, 'sequence_name', None)
        seq_name = repr (seq_name)
        (seqstr, extstr) = self.mk_seq_or_choice_str (node)
        self.output ("%sasn1.SEQUENCE ([%s], seq_name = %s)" %
                     (self.spaces (),seqstr, seq_name))
# XXX should output extstr
    def visitChoice (self, node):
        (ch_str, ext_str) = self.mk_seq_or_choice_str (node)
        self.output ("%sasn1.CHOICE ([%s])" % (self.spaces (), ch_str))
# XXX should output extstr

    def mk_tag_str(self, cls, tag_type, tag_num):
        # if this appears in input asn.1, I think we need to output
        # return str(tag_num) and ensure that asn1.CHOICE and asn1.SEQUENCE
        # and everything that might possibly take a NamedType with an explicit
        # tag handles it OK.
        raise NotImplementedError(cls, tag_type, tag_num)
    
    def visitElementType (self, node):
        # we have elt_type, val= named_type, maybe default=, optional=
        # named_type node: either ident = or typ =
        # need to dismember these in order to generate Python output syntax.
        nt = node.val
        assert (nt.type == 'NamedType')
        optflag = node.optional
        assert (node.default == None) # XXX add support for DEFAULT! 

        tagstr = 'None'
        identstr = nt.ident
        if hasattr (nt.typ, 'type') and nt.typ.type == 'tag': # ugh
            tagstr = self.mk_tag_str(nt.typ.tag.cls, # XXX
                                     nt.typ.tag.tag_typ,nt.typ.tag.num)
            nt = nt.typ
        typstr = self.visit_saving (nt.typ)
        self.output ("('%s',%s,%s,%d)" % (identstr, tagstr,typstr, optflag))
    def visitNamedType (self, node):
        typstr = self.visit_saving (node.typ)
        if node.ident != None:
            identstr = node.ident
        else:
            if hasattr (node.typ, 'val'):
                identstr = node.typ.val # unnamed choice arms default to name of type
            elif hasattr (node.typ, 'name'):
                identstr = node.typ.name
            else:
                identstr = self.make_new_name ()
        self.output ("('%s',None,%s)" % (identstr, typstr))

    def visitSubtype (self, node):
        pass
#        self.output ("#Ignoring subtype typ: %s" % repr(node)) # XXX
#        self.walker.dispatch (node.typ)
    def visitConstraint (self, node):
        pass
#        self.output ("#Ignoring constraint: %s" % repr(node))
#        self.walker.dispatch (node.subtype.typ)

def parse_and_output (s, fn, defined_dict):
    ast = compiler.yacc.parse (s)
    time_str = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    print("""#!/usr/bin/env python
# Auto-generated from %s at %s
from PyZ3950 import asn1""" % (fn, time_str))
    for module in ast:
        assert (module.type == 'Module')
        visit_instance = Visitor (defined_dict, fn)
        walker = visitor.ASTWalk ()
        visit_instance.set_walker (walker)
        walker.preorder (module, visit_instance)
        visit_instance.finish ()


import sys
if __name__ == '__main__':
    defined_dict = {}
    for fn in sys.argv [1:]:
        f = open (fn, "r")
        parse_and_output (f.read (), fn, defined_dict)
        f.close ()
        compiler.lexer.lineno = 1



