#!/usr/bin/env python

import sys
import visitor
import compiler
import time

# XXX should just calculate dependencies as we go along.  Should be part of prepass, not py-specific
def calc_dependencies (node, dict, trace = 0):
    if not hasattr (node, '__dict__'):
        if trace: print "#returning, node=", node
        return
    if node.type == 'Type_Ref': # XXX
        dict [node.name] = 1
        if trace: print "#Setting", node.name
        return
    for (a, val) in node.__dict__.items ():
        if trace: print "# Testing node ", node, "attr", a, " val", val
        if a[0] == '_':
            continue
        elif isinstance (val, type ([])):
            for v in val:
               calc_dependencies (v, dict, trace)
        else: # XXX should be subclass of node
            calc_dependencies (val, dict, trace)
    
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
        print self.text
    def spaces (self):
        return " " * (4 * self.indent_lev)
    def indent (self):
        self.indent_lev += 1
    def outdent (self):
        self.indent_lev -= 1
        assert (self.indent_lev >= 0)
    def register_assignment (self, ident, val, dependencies):
        if self.assignments.has_key (ident):
            raise "Duplicate assignment for " + ident
        if self.defined_dict.has_key (ident):
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
        assign_keys = self.assignments.keys()
        to_output_count = len (assign_keys)
        while 1:
            any_output = 0
            for (ident, val) in self.assignments.iteritems ():
                if already_output.has_key (ident):
                    continue
                ok = 1
                for d in self.dependencies [ident]:
                    if (not already_output.has_key (d) and
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
                cycle_list = []
                for ident in self.assignments.iterkeys ():
                    if not already_output.has_key (ident):
                        depend_list = [d for d in self.dependencies[ident] if d in assign_keys]
                        cycle_list.append ("%s(%s)" % (ident, ",".join (depend_list)))
                        
                text_list.append ("# Cycle XXX " + ",".join (cycle_list))
                for (ident, val) in self.assignments.iteritems ():
                    if not already_output.has_key (ident):
                        text_list.append ("%s=%s" % (ident, self.assignments [ident]))
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
        calc_dependencies (node.val, dep_dict, 0)
        depend_list = dep_dict.keys ()
        s = self.visit_saving (node.val)
        self.register_assignment (node.name.name, s,  depend_list)

    def visitValue_Assign (self, node):
        self.output ("Value_assign")
    def visitPyQuote (self, node):
        self.register_pyquote (node.val)
    def handleNamedNumList (self, node):
        def mk_named_num (nn):
            return "('%s',%s)" % (nn.ident, nn.val)
        names = ",".join (map (mk_named_num, node.named_list))
        self.output ("asn1.%s_class ([%s])" % (node.asn1_typ, names))
    visitInteger = handleNamedNumList
    visitBitString = handleNamedNumList

    def visitType_Ref (self, node):
        self.output (node.name)
    def visitSequence_Of (self, node):
        s = self.visit_saving (node.val)
        self.output ('%sasn1.SEQUENCE_OF (%s)' % (self.spaces (), s)) # XXX handle node.size_constr
        # XXX prefix w/ self.spaces for compatibility with old output, makes diffing
        # against old-style compiler's output easier

    def visitTag (self, node):
        # XXX should do tag number conversion to int earlier, in compiler!
        s = self.visit_saving (node.typ)
        val = int (node.tag.num)
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
    def visitSequence (self, node):
        # name, tag (None for no tag, EXPLICIT() for explicit), typ)
        # or '' + (1,) for optional
        seq_name = getattr (node, 'sequence_name', None)
        seq_name = repr (seq_name)
        self.indent ()
        def visit_list (l):
            slist = map (self.visit_saving, l)
            return (",\n%s"% self.spaces ()).join (slist)

        seqstr = visit_list (node.elt_list)
        if node.ext_list <> None:
            extstr = visit_list (node.ext_list)
        else:
            extstr = None
        self.outdent ()
        if extstr <> None:
            self.output ("%sasn1.SEQUENCE ([%s], ext=[%s], seq_name = %s)" % (
                self.spaces (), seqstr, extstr, seq_name))
        else:
            self.output ("%sasn1.SEQUENCE ([%s], seq_name = %s)" % (self.spaces (), 
                                                                    seqstr, seq_name))
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
            tagstr = mk_tag_str (self,nt.typ.tag.cls, # XXX
                                 nt.typ.tag.tag_typ,nt.typ.tag.num)
            nt = nt.typ
        typstr = self.visit_saving (nt.typ)
        self.output ("('%s',%s,%s,%d)" % (identstr, tagstr,typstr, optflag))
    def visitNamedType (self, node):
        typstr = self.visit_saving (node.typ)
        if node.ident <> None:
            identstr = node.ident
        else:
            if hasattr (node.typ, 'val'):
                identstr = node.typ.val # unnamed choice arms default to name of type
            elif hasattr (node.typ, 'name'):
                identstr = node.typ.name
            else:
                identstr = self.make_new_name ()
        self.output ("('%s',None,%s)" % (identstr, typstr))

    def visitChoice (self, node):
        self.indent ()
        def visit_list (l):
            slist = map (self.visit_saving, l)
            ret_str =  (",\n%s"% self.spaces ()).join (slist)
            return ret_str
            
        chstr = visit_list (node.elt_list)
        if node.ext_list <> None:
            extstr = visit_list (node.ext_list)
        else:
            extstr = None
        self.outdent ()
        if extstr <> None:
            self.output ("%sasn1.CHOICE ([%s], ext=[%s])" % (
                self.spaces (), chstr, extstr))
        else:
            self.output ("%sasn1.CHOICE ([%s])" % (
                self.spaces (), chstr))
    def visitSubtype (self, node):
        self.output ("#Ignoring subtype typ: %s" % str(self.spec)) # XXX
        self.walker.dispatch (self.typ)
    def visitConstraint (self, node):
        self.output ("#Ignoring constraint: %s" % str(self.type))
        self.walker.dispatch (self.subtype.typ)

def parse_and_output (s, fn, defined_dict):
    ast = compiler.yacc.parse (s)
    time_str = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    print """#!/usr/bin/env python
# Auto-generated from %s at %s
from PyZ3950 import asn1""" % (fn, time_str)
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



