#!/usr/bin/env python

"""Implements part of CCL, the Common Command Language, ISO 8777.  I'm
working from the description in the YAZ toolkit
(http://www.indexdata.dk/yaz/doc/tools.php), rather than the ISO
spec.  Two extensions:
- qualifiers can be literal "(attrtyp, attrval)" pairs, so, e.g., the
following is a legitimate for ISBN: "(1,7)=0312033095"
- the optional ATTRSET (attrset/query) which must appear at the beginning
of the string.
Allowed values are:
BIB1 (default)
XD1
UTIL
ZTHES1
EXP1
or an oid expressed as a dotted string.  (A leading dot implies a
prefix of 1.2.840.1003.3, so, e.g., .1 is the same as BIB1.)

Eventually I will support v3-style mixing attribute sets within
a single query, but for now I don't.
"""

from __future__ import nested_scopes
import string

in_setup = 0

try:
    from PyZ3950 import z3950
    from PyZ3950 import oids
    from PyZ3950 import asn1

    _attrdict = {
        'bib1'  :  oids.Z3950_ATTRS_BIB1_ov,
        'zthes1': oids.Z3950_ATTRS_ZTHES_ov,
        'xd1': oids.Z3950_ATTRS_XD1_ov,
        'utility': oids.Z3950_ATTRS_UTIL_ov,
        'exp1':  oids.Z3950_ATTRS_EXP1_ov
        }
    
except ImportError, err:
    print "Error importing (OK during setup)", err
    in_setup = 1

class QuerySyntaxError(Exception): pass
class ParseError(QuerySyntaxError): pass
class LexError(QuerySyntaxError): pass
class UnimplError(QuerySyntaxError): pass

tokens = ('LPAREN', 'RPAREN', 'COMMA',
          'SET', 'ATTRSET','QUAL',  'QUOTEDVALUE', 'RELOP',  'WORD',
          'LOGOP', 'SLASH')

t_LPAREN= r'\('
t_RPAREN= r'\)'
t_COMMA = r','
t_SLASH = r'/'
def t_ATTRSET(t):
    r'(?i)ATTRSET'
    return t

def t_SET (t): # need to def as function to override parsing as WORD, gr XXX
    r'(SET)'
    return t

relop_to_attrib = {
    '<': 1,
    '<=': 2,
    '=': 3,
    '>=': 4,
    '>': 5,
    '<>': 6}

t_RELOP = "|".join (["(%s)" % r for r in relop_to_attrib.keys()])
# XXX Index Data docs say 'doesn't follow ... ISO8777'?

# XXX expand to rd. addt'l defns from file?

qual_dict = { # These are bib-1 attribute values, see
# http://www.loc.gov/z3950/agency/defns/bib1.html and  ftp://ftp.loc.gov/pub/z3950/defs/bib1.txt
    'TI': (1,4),
    'AU': (1,1003), # use 1003 to work w/ both NLC-BNC and LC
    'ISBN': (1,7),
    'LCCN': (1,9),
    'ANY': (1,1016),
    'FIF': (3, 1), # first-in-field
    'AIF': (3,3), # any-in-field (default)
    'RTRUNC': (5,1),
    'NOTRUNC': (5,100) # (default)
    }
default_quals = ['ANY'] # XXX should be per-attr-set
default_relop = '='

def t_QUAL(t):
    return t

def mk_quals ():
    quals = ("|".join (map (lambda x: '(' + x + ')', qual_dict.keys())))
    t_QUAL.__doc__ = "(?i)" + quals + r"|(\([0-9]+,[0-9]+\))"

def t_QUOTEDVALUE(t):
    r"(\".*?\")"
    if t.value[0] == '"':
        t.value = t.value[1:-1]
    return t

word_init = "[a-z]|[A-Z]|[0-9]|&|:"
word_non_init = ",|\.|\'"

t_WORD = "(%s)(%s|%s)*" % (word_init, word_init, word_non_init)

def t_LOGOP(t):
    r'(?i)(AND)|(OR)|(NOT)'
    return t


t_ignore = " \t"

def t_error(t):
    raise LexError ('t_error: ' + str (t))

    
import lex



def relex ():
    global lexer
    mk_quals ()
    lexer = lex.lex()

relex ()

def add_qual (qual_name, val):
    """Add a qualifier definition, and regenerate the lexer."""
    qual_dict[qual_name] = val
    relex ()

import yacc

#if in_setup:
#    import yacc
#else:
#    from PyZ3950 import yacc

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf
    def str_child (self, child, depth):
        if isinstance (child, Node): # ugh
            return child.str_depth (depth)
        indent = " " * (4 * depth)
        return indent + str (child) + "\n"
    def str_depth (self, depth): # ugh
        indent = " " * (4 * depth)
        l = ["%s%s %s" % (indent, self.type, self.leaf)]
        l.append ("".join (map (lambda s: self.str_child (s, depth + 1),
                                self.children)))
        return "\n".join (l)
    def __str__(self):
        return "\n" + self.str_depth (0)

def p_top (t):
    'top : cclfind_or_attrset'
    t[0] = t[1]
    
def p_cclfind_or_attrset_1 (t):
    'cclfind_or_attrset : cclfind'
    t[0] = t[1]

def p_cclfind_or_attrset_2 (t):
    'cclfind_or_attrset : ATTRSET LPAREN WORD SLASH cclfind RPAREN'
    t[0] = Node ('attrset', [t[5]], t[3])
        
def p_ccl_find_1(t):
    'cclfind : cclfind LOGOP elements'
    t[0] = Node ('op', [t[1],t[3]], t[2])

def p_ccl_find_2(t):
    'cclfind : elements'
    t[0] = t[1]

def p_elements_1(t):
    'elements : LPAREN cclfind RPAREN'
    t[0] = t[2]

class QuallistVal:
    def __init__ (self, quallist, val):
        self.quallist = quallist
        self.val = val
    def __str__ (self):
        return "QV: %s %s" % (str(self.quallist),str (self.val))
    def __getitem__ (self, i):
        if i == 0: return self.quallist
        if i == 1: return self.val
        raise IndexError ('QuallistVal err ' + str (i))
    
def xlate_qualifier (x):
    if x[0] == '(' and x[-1] == ')':
        t = x[1:-1].split (',') # t must be of len 2 b/c of lexer
        return (string.atoi (t[0]), string.atoi (t[1]))
    return qual_dict[(x.upper ())]


def p_elements_2 (t):
    'elements : SET RELOP WORD'
    if t[2] <> '=':
        raise QuerySyntaxError (str (t[1], str (t[2]), str (t[3])))
    t[0] = Node ('set', leaf = t[3])

def p_elements_3(t):
    'elements : val'
    t[0] = Node ('relop', QuallistVal (map (xlate_qualifier, default_quals), t[1]), default_relop)

def p_elements_4(t):
    'elements : quallist RELOP val'
    t[0] = Node ('relop', QuallistVal(map (xlate_qualifier, t[1]),t[3]), t[2])
    
# XXX p_elements_5 would be quals followed by recursive def'n, not yet implemented
# XXX p_elements_6 would be quals followed by range, not yet implemented.

def p_quallist_1 (t):
    'quallist : QUAL'
    t[0] = [t[1]]

def p_quallist_2 (t):
    'quallist : quallist COMMA QUAL'
    t[0] = t[1] + [t[3]]

def p_val_1(t):
    'val : QUOTEDVALUE'
    t[0] = t[1]
    
def p_val_2(t):
    'val : val WORD'
    t[0] = t[1] + " " + t[2]
    
def p_val_3(t):
    'val : WORD'
    t[0] = t[1]


# XXX also don't yet handle proximity operator

def p_error(t):
    raise ParseError ('Parse p_error ' + str (t))

precedence = (
    ('left', 'LOGOP'),
    )

yacc.yacc (debug=0, tabmodule = 'PyZ3950_parsetab')
#yacc.yacc (debug=0, tabpackage = 'PyZ3950', tabmodule='PyZ3950_parsetab')


def attrset_to_oid (attrset):
    l = attrset.lower ()
    if _attrdict.has_key (l):
        return _attrdict [l]
    split_l = l.split ('.')
    if split_l[0] == '':
        split_l = oids.Z3950_ATTRS + split_l[1:]
    try:
        intlist = map (string.atoi, split_l)
    except ValueError:
        raise ParseError ('Bad OID: ' + l)
    return asn1.OidVal (intlist)


def tree_to_q (ast):
    if ast.type == 'op':
        myrpnRpnOp = z3950.RpnRpnOp ()
        myrpnRpnOp.rpn1 = tree_to_q(ast.children[0])
        myrpnRpnOp.rpn2 = tree_to_q(ast.children[1])
        op = ast.leaf.lower ()
        if op == 'not': op = 'and-not' # CCL spec of 'not' vs. Z39.50 spec of 'and-not'
        myrpnRpnOp.op = (op, None)
        return ('rpnRpnOp', myrpnRpnOp)
    elif ast.type == 'relop':
        # XXX but e.g. LC (http://lcweb.loc.gov/z3950/lcserver.html)
        # doesn't support other relation attributes, either.
        try:
            relattr = relop_to_attrib [ast.leaf]
        except KeyError:  # should never happen, how could we have lexed it?
            raise UnimplError (ast.leaf)
        def make_aelt (qual):
            val = ('numeric', qual [1])
            return z3950.AttributeElement (attributeType = qual[0],
                                           attributeValue = val)
        apt  = z3950.AttributesPlusTerm ()
        quallist = ast.children.quallist
        if ast.leaf <> '=':
            quallist.append ((2,relattr)) # 2 is relation attribute
            # see http://www.loc.gov/z3950/agency/markup/13.html ATR.1.1
        apt.attributes = map (make_aelt, quallist)
        apt.term = ('general', ast.children.val) # XXX update for V3?
        return ('op', ('attrTerm', apt))
    elif ast.type == 'set':
        return ('op', ('resultSet', ast.leaf))
        
    raise UnimplError("Bad ast type " + str(ast.type))

def mk_rpn_query (query):
    """Transform a CCL query into an RPN query."""
    # need to copy or create a new lexer because it contains globals
    # PLY 1.0 lacks __copy__
    # PLY 1.3.1-1.5 have __copy__, but it's broken and returns None
    # I sent David Beazley a patch, so future PLY releases will
    # presumably work correctly.
    # Recreating the lexer each time is noticeably slower, so this solution
    # is suboptimal for PLY <= 1.5, but better than being thread-unsafe.
    # Perhaps I should have per-thread lexer instead XXX
    # with example/twisted/test.py set to parse_only, I get 277 parses/sec
    # with fixed PLY, vs. 63 parses/sec with broken PLY, on my 500 MHz PIII
    # laptop.
    
    copiedlexer = None
    if hasattr (lexer, '__copy__'):
        copiedlexer = lexer.__copy__ ()
    if copiedlexer == None:
        copiedlexer = lex.lex ()
    ast = yacc.parse (query, copiedlexer)
    return ast_to_rpn (ast)

def ast_to_rpn (ast):
    if ast.type == 'attrset':
        attrset = attrset_to_oid (ast.leaf)
        ast = ast.children [0]
    else:
        attrset = oids.Z3950_ATTRS_BIB1_ov
    rpnq = z3950.RPNQuery (attributeSet = attrset)
    rpnq.rpn = tree_to_q (ast)
    return ('type_1', rpnq)

def testlex (s):
    lexer.input (s)
    while 1:
        token = lexer.token ()
        if not token:
            break
        print token
            
def testyacc (s):
    copylex = lexer.__copy__ ()
    ast = yacc.parse (s, lexer = copylex)
    print "AST:", ast
    print "RPN Query:", ast_to_rpn (ast)

if __name__ == '__main__':
    testfn = testyacc
    #    testfn = testlex
    testfn ('attrset (BIB1/ au="Gaiman, Neil" or ti=Sandman)')
    while 1:
        s = raw_input ('Query: ')
        if len (s) == 0:
            break
        testfn (s)
#    testyacc ()
#    testlex ()
