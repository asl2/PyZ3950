#!/usr/bin/env python


import visitor

"""Compiler from ASN.1 specification to the Python format acceptable
to my asn1.py module.  Loosely based on esnacc grammar.  We ignore
MACROs, CONSUMER INVOKES, SUPPLIER INVOKES, and a lot of stuff, for simplicity.

We also ignore the {...} syntax for basic values, so we don't need separate
lexer states.
"""

# TODO:
# toposort structures, handle recursive structures better than PyQuote hack
# figure out mapping of asn.1 modules to python modules (probably as classes)
# handle int_2/num_list
# handle ANY, ANY DESCRIBED BY
# we replace '-' in idents w/ '_' during lexing.  Is this OK, or should it be done at output?


class LexError(Exception): pass
class ParseError(Exception): pass

static_tokens = {
    '\.' : 'DOT',
    ','  : 'COMMA',
    '\{' : 'LBRACE',
    '\}' : 'RBRACE',
    '\(' : 'LPAREN',
    '\)' : 'RPAREN',
    '\[' : 'LBRACK',
    '\]' : 'RBRACK',
    '<'  : 'LT',
    '-'  : 'MINUS',
    '\.\.' : 'RANGE',
    '\.\.\.' : 'ELLIPSIS',
    '::=': 'GETS',
    '\|' : 'BAR',
    ';'  : 'SEMICOLON'

    }

# all keys in reserved_words must start w/ upper case
reserved_words = {
    'TAGS' : 'TAGS',
    'BOOLEAN' : 'BOOLEAN',
    'INTEGER' : 'INTEGER',
    'BIT'     : 'BIT',
    'STRING'  : 'STRING',
    'OCTET'   : 'OCTET',
    'NULL'    : 'NULL',
    'SEQUENCE': 'SEQUENCE',
    'OF'      : 'OF',
    'SET'     : 'SET',
    'IMPLICIT': 'IMPLICIT',
    'CHOICE'  : 'CHOICE',
    'ANY'     : 'ANY',
    'EXTERNAL' : 'EXTERNAL', # XXX added over base
    'OPTIONAL':'OPTIONAL',
    'DEFAULT' : 'DEFAULT',
    'COMPONENTS': 'COMPONENTS',
    'UNIVERSAL' : 'UNIVERSAL',
    'APPLICATION' : 'APPLICATION',
    'PRIVATE'   : 'PRIVATE',
    'TRUE' : 'TRUE',
    'FALSE' : 'FALSE',
    'BEGIN' : 'BEGIN',
    'END' : 'END',
    'DEFINITIONS' : 'DEFINITIONS',
    'EXPLICIT' : 'EXPLICIT',
    'ENUMERATED' : 'ENUMERATED',
    'EXPORTS' : 'EXPORTS',
    'IMPORTS' : 'IMPORTS',
    'REAL'    : 'REAL',
    'INCLUDES': 'INCLUDES',
    'MIN'     : 'MIN',
    'MAX'     : 'MAX',
    'SIZE'    : 'SIZE',
    'FROM'    : 'FROM',
    'WITH'    : 'WITH',
    'COMPONENT': 'COMPONENT',
    'PRESENT'  : 'PRESENT',
    'ABSENT'   : 'ABSENT',
    'DEFINED'  : 'DEFINED',
    'BY'       : 'BY',
    'PLUS-INFINITY'   : 'PLUS_INFINITY',
    'MINUS-INFINITY'  : 'MINUS_INFINITY',
    'GeneralizedTime' : 'GENERALIZEDTIME',
    'UTCTime'         : 'UTCTIME',
    'ObjectDescriptor': 'OBJECTDESCRIPTOR',
    'AUTOMATIC': 'AUTOMATIC',
#      'OPERATION'       : 'OPERATION',
#      'ARGUMENT'        : 'ARGUMENT',
#      'RESULT'          : 'RESULT',
#      'ERRORS'          : 'ERRORS',
#      'LINKED'          : 'LINKED',
#      'ERROR'           : 'ERROR',
#      'PARAMETER'       : 'PARAMETER',
#      'BIND'            : 'BIND',
#      'BIND-ERROR'      : 'BIND_ERROR',
#      'UNBIND'          : 'UNBIND',
#      'APPLICATION-CONTEXT' : 'AC',
#      'APPLICATON-SERVICE-ELEMENTS' : 'ASES',
#      'REMOTE' : 'REMOTE',
#      'INITIATOR' : 'INITIATOR',
#      'RESPONDER' : 'RESPONDER',
#      'APPLICATION-SERVICE-ELEMENT' : 'ASE',
#      'OPERATIONS' : None,
#      'EXTENSION-ATTRIBUTE' : 'EXTENSION_ATTRIBUTE',
#      'EXTENSIONS' : None,
#      'CHOSEN' : None,
#      'EXTENSION' : None,
#      'CRITICAL': None,
#      'FOR' : None,
#      'SUBMISSION' : None,
#      'DELIVERY' : None,
#      'TRANSFER' : None,
#      'OBJECT' : None,
#      'PORTS' : None,
#      'PORT'  : None,
#      r'ABSTRACT\s*OPERATIONS' : 'ABSTR_OPS',
#      'REFINE' : None,
#      'AS' : None,
#      'RECURRING' : None
    }

for k in list(static_tokens.keys ()):
    if static_tokens [k] == None:
        static_tokens [k] = k

StringTypes = ['Numeric', 'Printable', 'IA5', 'BMP', 'Universal', 'UTF8',
               'Teletex', 'T61', 'Videotex', 'Graphics', 'ISO646', 'Visible',
               'General']

string_tok_names = [x + 'String' for x in StringTypes]


tokens = list(static_tokens.values ()) + ['OBJECT_IDENTIFIER', 'STRING_T',
                                    'BSTRING', 'HSTRING', 'QSTRING',
                                    'UCASE_IDENT', 'LCASE_IDENT',
                                    'NUMBER', 'PYQUOTE']  + list(reserved_words.values ())

def t_OBJECT_IDENTIFIER (t):
    r"OBJECT\s+IDENTIFIER"
    return t

def t_STRING_T(t):
    return t

t_STRING_T.__doc__ = "(%s)String" % "|".join (['(' + x + ')' for x in StringTypes])

cur_mod = __import__ (__name__) # XXX blech!

for (k, v) in list(static_tokens.items ()):
    cur_mod.__dict__['t_' + v] = k

def t_BSTRING (t):
    r"'[01]*'B"
    return t

def t_HSTRING (t):
    r"'[0-9A-Fa-f]*'H"
    return t

def t_QSTRING (t):
    r'"([^"]|"")*"'
    return t # XXX might want to un-""

def t_UCASE_IDENT (t):
    r"[A-Z](-[a-zA-Z0-9]|[a-zA-Z0-9])*" # can't end w/ '-'
    t.type = reserved_words.get (t.value, "UCASE_IDENT")
    t.value = t.value.replace ('-', '_') # XXX is it OK to do '-' to '_' during lex
    return t

def t_LCASE_IDENT (t):
    r"[a-z](-[a-zA-Z0-9]|[a-zA-Z0-9])*" # can't end w/ '-'
    t.value = t.value.replace ('-', '_')# XXX is it OK to do '-' to '_' during lex
    return t

def t_NUMBER (t):
    r"0|([1-9][0-9]*)"
    return t

pyquote_str = 'PYQUOTE'
def t_COMMENT(t):
    r"--(-[^\-\n]|[^\-\n])*(--|\n|-\n)"
    if (t.value.find("\n") >= 0) : t.lineno += 1
    if t.value[2:2+len (pyquote_str)] == pyquote_str:
        t.value = t.value[2+len(pyquote_str):]
        t.value = t.value.lstrip ()
        t.type = pyquote_str
        return t
    return None

t_ignore = " \t\r"

def t_NEWLINE(t):
    r'\n+'
    t.lineno += t.value.count("\n")

def t_error(t):
    print("Error", repr(t.value[:100]), t.lineno)
    raise LexError

    
import lex
lexer = lex.lex()

import yacc

class Node:
    def __init__(self,*args, **kw):
        if len (args) == 0:
            self.type = self.__class__.__name__
        else:
            assert (len(args) == 1)
            self.type = args[0]
        self.__dict__.update (kw)
    def str_child (self, key, child, depth):
        if key == 'type': # already processed in str_depth
            return ""
        if isinstance (child, Node): # ugh
            return child.str_depth (depth)
        indent = " " * (4 * depth)
        keystr = indent + key + ":\n"
        if type (child) == type ([]):
            return keystr + indent.join (map (str, child)) + "\n"
        else:
            return keystr + indent + str (child) + "\n"
    def str_depth (self, depth): # ugh
        indent = " " * (4 * depth)
        l = ["%s%s" % (indent, self.type)]
        l.append ("".join ([self.str_child (k_v[0], k_v[1], depth + 1) for k_v in list(self.__dict__.items ())]))
        return "\n".join (l)
    def get_typ (self):
        return self
    def set_name (self, name): # only overridden for SEQUENCE
        pass
    def __str__(self):
        return "\n" + self.str_depth (0)

class Module (Node):
    pass

class ModuleIdent (Node):
    pass

class Module_Body (Node):
    pass

class Default_Tags (Node):
    pass

class Type_Assign (Node):
    def __init__ (self, *args, **kw):
        Node.__init__ (self, *args, **kw)
        to_test = self.val.get_typ ()
        to_test.set_name (self.name.name) # currently only for naming SEQUENCE
        # for debugging purposes
        # XXX should also collect names for SEQUENCE inside SEQUENCE or
        # CHOICE or SEQUENCE_OF (where should the SEQUENCE_OF name come
        # from?  for others, element or arm name would be fine)

class PyQuote (Node):
    pass

class Type_Ref (Node):
    pass
    
class Sequence_Of (Node):
    pass

class Set_Of (Node):
    pass

class Tag (Node):
    def get_typ (self):
        return self.typ

class ElementType(Node):
    pass

class Sequence (Node):
    def set_name (self, name):
        self.sequence_name = name
    
class Choice (Node):
    pass

class Subtype (Node):
    pass

class Size(Node):
    pass

class From(Node):
    pass
    
class Constraint (Node):
    pass

class Enum (Node):
    pass

class Literal (Node):
    pass

class NamedNumber (Node):
    pass

class NamedNumListBase(Node):
    pass

class ValueRange(Node):
    pass

class Integer (NamedNumListBase):
    asn1_typ = 'INTEGER'

class BitString (NamedNumListBase):
    asn1_typ = 'BITSTRING'

class NamedType (Node):
    pass

class BaseType (Node):
    pass
    
def p_module_list_1 (t):
    'module_list : module_list module_def'
    t[0] = t[1] + [t[2]]

def p_module_list_2 (t):
    'module_list : module_def'
    t[0] = [t[1]]

def p_module_def (t):
    'module_def : module_ident DEFINITIONS tag_default GETS BEGIN module_body END'
    body = t[6]
    t[0] = Module (ident = t[1], tag_def = t[3],
                   exports = body.exports, imports = body.imports, assign_list = body.assign_list)

def p_tag_default_1 (t):
    '''tag_default : EXPLICIT TAGS
    | IMPLICIT TAGS
    | AUTOMATIC TAGS'''
    t[0] = Default_Tags (dfl_tag = t[1])

def p_tag_default_2 (t):
    'tag_default : '
    t[0] = Default_Tags (dfl_tag = 'EXPLICIT')

def p_module_ident (t):
    'module_ident : type_ref assigned_ident' # name, oid
    # XXX coerce type_ref to module_ref?
    if t[2] == None:
        t[0] = ModuleIdent (name=t[1].name, assigned_ident = None)
    else:
        t[0] = ModuleIdent (name=t[1].name, assigned_ident = t[2])

# XXX originally we had both type_ref and module_ref, but that caused
# a reduce/reduce conflict (because both were UCASE_IDENT).  Presumably
# this didn't cause a problem in the original ESNACC grammar because it
# was LALR(1) and PLY is (as of 1.1) only SLR.

#def p_module_ref (t):
#    'module_ref : UCASE_IDENT'
#    t[0] = t[1]

def p_assigned_ident_1 (t):
    'assigned_ident : oid_val'
    t[0] = t[1]

def p_assigned_ident_2 (t):
    'assigned_ident : '
    t[0] = None

def p_module_body_1 (t):
    'module_body : exports imports assign_list'
    t[0] = Module_Body (exports = t[1], imports = t[2], assign_list = t[3])

def p_module_body_2 (t):
    'module_body : '
    t[0] = Module_Body (exports = [], imports = [], assign_list = [])

def p_exports_1 (t):
    'exports : EXPORTS syms_exported SEMICOLON'
    t[0] = t[2]

def p_exports_2 (t):
    'exports : '
    t[0] = []

def p_syms_exported_1 (t):
    'syms_exported : exp_sym_list'
    t[0] = t[1]

def p_syms_exported_2 (t):
    'syms_exported : '
    t[0] = []

def p_exp_sym_list_1 (t):
    'exp_sym_list : symbol'
    t[0] = [t[1]]

def p_exp_sym_list_2 (t):
    'exp_sym_list : exp_sym_list COMMA symbol'
    t[0] = t[1] + [t[3]]
    
def p_imports_1(t):
    'imports : IMPORTS syms_imported SEMICOLON'
    t[0] = t[2]

def p_imports_2 (t):
    'imports : '
    t[0] = []

def p_syms_imported_1(t):
    'syms_imported : '
    t[0] = []

def p_syms_imported_2 (t):
    'syms_imported : syms_from_module_list'
    t[0] = t[1]

def p_syms_from_module_list_1 (t):
    'syms_from_module_list : syms_from_module_list syms_from_module'
    t[0] = t[1] + [t[2]]

def p_syms_from_module_list_2 (t):
    'syms_from_module_list : syms_from_module'
    t[0] = [t[1]]

def p_syms_from_module (t):
    'syms_from_module : symbol_list FROM module_ident'
    t[0] = Node ('syms_list', symbol_list = t[1], module = t[3])

def p_symbol_list_1 (t):
    '''symbol_list : symbol_list COMMA symbol'''
    t[0] = t[1] + [t[3]]

def p_symbol_list_2 (t):
    'symbol_list : symbol'
    t[0] = [t[1]]

def p_symbol (t):
    '''symbol : type_ref
    | identifier''' # XXX omit DefinedMacroName
    t[0] = t[1]

def p_assign_list_1 (t):
    'assign_list : assign_list assign'
    t[0] = t[1] + [t[2]]

def p_assign_list_2 (t):
    'assign_list : assign SEMICOLON'
    t[0] = [t[1]]

def p_assign_list_3 (t):
    'assign_list : assign'
    t[0] = [t[1]]

def p_assign (t):
      '''assign : type_assign
      | value_assign
      | pyquote'''
      t[0] = t[1]

def p_pyquote (t):
    '''pyquote : PYQUOTE'''
    t[0] = PyQuote (val = t[1])


def p_type_assign (t):
    'type_assign : type_ref GETS type'
    t[0] = Type_Assign (name = t[1], val = t[3])

def p_type (t): # XXX ignore DefinedMacroType
    '''type : builtin_type
    | defined_type
    | sub_type'''
    t[0] = t[1]

def p_ext_type_ref (t):
    'ext_type_ref : type_ref DOT type_ref'
    # XXX coerce 1st type_ref to module_ref
    t[0] = Node ('ext_type_ref', module = t[1], typ = t[3])

def p_defined_type (t): # XXX old comment: could by CharacterString or Useful types too
    '''defined_type : ext_type_ref
    | type_ref'''
    t[0] = t[1]

def p_builtin_type_1 (t):
    '''builtin_type : boolean_type
    | integer_type
    | bitstring_type
    | null_type
    | sequence_type
    | sequenceof_type
    | set_type
    | setof_type
    | choice_type
    | selection_type
    | tagged_type
    | any_type
    | oid_type
    | enum_type
    | real_type
    | char_str_type
    | useful_type'''
    t[0] = t[1]

def p_builtin_type_2 (t):
    'builtin_type : OCTET STRING'
    t[0] = BaseType (val = 'OCTSTRING')


def p_named_type_1 (t):
    'named_type : identifier type'
    t[0] = NamedType (ident = t[1], typ = t[2])

def p_named_type_2 (t):
    'named_type : type' # XXX handles selectionType as well old comment??
    t[0] = NamedType (ident = None, typ = t[1])

def p_boolean_type (t):
    'boolean_type : BOOLEAN'
    t[0] = BaseType (val = 'BOOLEAN')

def p_integer_type_1 (t):
    'integer_type : INTEGER'
    t[0] = Integer (named_list = [])

def p_integer_type_2 (t):
    'integer_type : INTEGER LBRACE named_number_list RBRACE'
    t[0] = Integer (named_list = t[3])

def p_named_number_list_1 (t):
    'named_number_list : named_number_list COMMA named_number'
    t[0] = t[1] + [t[3]]

def p_named_number_list_2 (t):
    'named_number_list : named_number'
    t[0] = [t[1]]

def p_named_number (t):
    '''named_number : identifier LPAREN signed_number RPAREN
    | identifier LPAREN defined_value RPAREN'''
    t[0] = NamedNumber (ident = t[1], val = t[3])

# XXX numbers used to errchk for 32-bit ranged
def p_signed_number_1 (t):
    'signed_number : NUMBER'
    t[0] = t [1]

def p_signed_number_2 (t):
    'signed_number : MINUS NUMBER'
    t[0] = '-' + t[2]

def p_enum_type_1 (t):
    'enum_type : ENUMERATED LBRACE named_number_list RBRACE'
    t[0] = Enum (val = t[3])

def p_enum_type_2 (t):
    'enum_type : ENUMERATED LBRACE named_number_list COMMA ELLIPSIS RBRACE'
    t[0] = Enum (val = t[3], ext=[])

def p_real_type (t):
    'real_type : REAL'
    t[0] = BaseType (val = 'REAL')

def p_bitstring_type_1 (t):
    'bitstring_type : BIT STRING'
    t[0] = BitString (named_list = [])

def p_bitstring_type_2 (t):
    'bitstring_type : BIT STRING LBRACE named_bit_list RBRACE'
    t[0] = BitString (named_list = t[4])

def p_named_bit_list (t):
    'named_bit_list : named_number_list'
    t[0] = t[1]

def p_null_type (t):
    'null_type : NULL'
    t[0] = BaseType (val='NULL')

def p_sequence_type (t):
    'sequence_type : SEQUENCE LBRACE component_type_lists RBRACE'
    # XXX 
    if isinstance (t[3], list):
        assert (len (t[3]) == 0)
        t[0] = Sequence (elt_list=[], ext_list = None)
    else:
        if 'ext_list' in t[3]:
            t[0] = Sequence (elt_list = t[3]['elt_list'], ext_list = t[3]['ext_list'])
        else:
            t[0] = Sequence (elt_list = t[3]['elt_list'], ext_list = None)

def p_sequence_type_2 (t):
    'sequence_type : SEQUENCE LBRACE RBRACE'
    t[0] = Sequence (elt_list=[], ext_list  =None)


def p_extension_and_exception_1 (t):
    'extension_and_exception : ELLIPSIS'
    t[0] = []

def p_optional_extension_marker_1 (t):
    'optional_extension_marker : COMMA ELLIPSIS'
    t[0] = True

def p_optional_extension_marker_2 (t):
    'optional_extension_marker : '
    t[0] = False

def p_component_type_lists_1 (t):
    'component_type_lists : element_type_list'
    t[0] = {'elt_list' : t[1]}

def p_component_type_lists_2 (t):
    '''component_type_lists : element_type_list COMMA extension_and_exception extension_additions optional_extension_marker'''
    t[0] = {'elt_list' : t[1], 'ext_list' : t[4]}

def p_component_type_lists_3 (t):
    '''component_type_lists : extension_and_exception extension_additions optional_extension_marker'''
    t[0] = []

def p_extension_additions_1 (t):
    'extension_additions : extension_addition_list'
    t[0] = t[1]

def p_extension_additions_2 (t):
    'extension_additions : '
    t[0] = []

def p_extension_addition_list_1 (t):
    'extension_addition_list : COMMA extension_addition'
    t[0] = [t[2]]

def p_extension_addition_list_2 (t):
    'extension_addition_list : extension_addition_list COMMA extension_addition'
    t[0] = t[1] + [t[3]]

def p_extension_addition_1 (t):
    'extension_addition : element_type'
    t[0] = t[1]

def p_element_type_list_1 (t):
    'element_type_list : element_type'
    t[0] = [t[1]]

def p_element_type_list_2 (t):
    'element_type_list : element_type_list COMMA element_type'
    t[0] = t[1] + [t[3]]


def p_element_type_1 (t):
    'element_type : named_type'
    t[0] = ElementType (val = t[1], optional = 0, default = None)

def p_element_type_2 (t):
    'element_type : named_type OPTIONAL'
    t[0] = ElementType (val = t[1], optional = 1, default = None)

def p_element_type_3 (t):
    'element_type : named_type DEFAULT named_value'
    t[0] = ElementType (val = t[1], optional = 1, default = t[3])
#          /*
#           * this rules uses NamedValue instead of Value
#           * for the stupid choice value syntax (fieldname value)
#           * it should be like a set/seq value (ie with
#           * enclosing { }
#           */

# XXX get to COMPONENTS later

def p_sequenceof_type (t):
    'sequenceof_type : SEQUENCE OF type'
    t[0] = Sequence_Of (val = t[3], size_constr = None)

def p_set_type (t):
    'set_type : SET LBRACE element_type_list RBRACE'
    t[0] = Node ('set', val = t[3])

def p_setof_type (t):
    'setof_type : SET OF type'
    t[0] = Set_Of (val=t[3])

def p_choice_type (t):
    'choice_type : CHOICE LBRACE alternative_type_lists RBRACE'
    if 'ext_list' in t[3]:
        t[0] = Choice (elt_list = t[3]['elt_list'], ext_list = t[3]['ext_list'])
    else:
        t[0] = Choice (elt_list = t[3]['elt_list'], ext_list = None)

def p_alternative_type_lists_1 (t):
    'alternative_type_lists : alternative_type_list'
    t[0] = {'elt_list' : t[1]}

def p_alternative_type_lists_2 (t):
    '''alternative_type_lists : alternative_type_list COMMA extension_and_exception extension_addition_alternatives optional_extension_marker'''
    t[0] = {'elt_list' : t[1], 'ext_list' : t[4]}

def p_extension_addition_alternatives_1 (t):
    'extension_addition_alternatives : extension_addition_alternatives_list'
    t[0] = t[1]

def p_extension_addition_alternatives_2 (t):
    'extension_addition_alternatives : '
    t[0] = []

def p_extension_addition_alternatives_list_1 (t):
    'extension_addition_alternatives_list : COMMA extension_addition_alternative'
    t[0] = [t[2]]

def p_extension_addition_alternatives_list_2 (t):
    'extension_addition_alternatives_list : extension_addition_alternatives_list COMMA extension_addition_alternative'
    t[0] = t[1] + [t[3]]

def p_extension_addition_alternative_1 (t):
    'extension_addition_alternative : named_type'
    t[0] = t[1]

def p_alternative_type_list_1 (t):
    'alternative_type_list : named_type'
    t[0] = [t[1]]

def p_alternative_type_list_2 (t):
    'alternative_type_list : alternative_type_list COMMA named_type'
    t[0] = t[1] + [t[3]]

def p_selection_type (t):
    'selection_type : identifier LT type'
    return Node ('seltype', ident = t[1], typ = t[3])

def p_tagged_type_1 (t):
    'tagged_type : tag type'
    t[0] = Tag (tag_typ = 'default', tag = t[1], typ = t[2])
    
def p_tagged_type_2 (t):
    'tagged_type : tag IMPLICIT type'
    t[0] = Tag (tag_typ = 'implicit', tag = t[1], typ = t[3])

def p_tagged_type_3 (t):
    'tagged_type : tag EXPLICIT type'
    t[0] = Tag (tag_typ = 'explicit', tag = t[1], typ = t[3])


def p_tag (t):
    'tag : LBRACK class class_number RBRACK'
    t[0] = Node ('tag', cls = t[2], num = int(t[3]))
# XXX should verify uniqueness of APPLICATION tags per-module

def p_class_number_1 (t):
    'class_number : number'
    t[0] = t[1]

def p_class_number_2 (t):
    'class_number : defined_value'
    t[0] = t[1]

def p_class_1 (t):
    '''class : UNIVERSAL
    | APPLICATION
    | PRIVATE'''
    t[0] = t[1]

def p_class_2 (t):
    '''class : '''
    t[0] = 'CONTEXT'

def p_any_type_1 (t):
    'any_type : ANY'
    t[0] = BaseType (val='ANY')

def p_any_type_2 (t):
    'any_type : ANY DEFINED BY identifier'
    t[0] = Literal (val='asn1.ANY_constr(def_by="%s")' % t[4]) # XXX

def p_oid_type (t):
    'oid_type : OBJECT_IDENTIFIER'
    t[0] = BaseType (val='OBJECT_IDENTIFIER') # XXX

def p_useful_type (t):
    '''useful_type : GENERALIZEDTIME
    | UTCTIME
    | OBJECTDESCRIPTOR
    | EXTERNAL'''
    t[0] = BaseType (val = t[1])

def p_char_str_type (t):
    'char_str_type : STRING_T'
    t[0] = BaseType (val = t[1])

def p_sub_type_1 (t):
    'sub_type : type subtype_spec'
    t[0] = t[1]
    t[0].subtype = t[2]

def p_sub_type_2 (t):
    'sub_type : SET size_constraint OF type'
    t[0] = Set_Of (val=t[4], subtype = t[2])
    t[0].subtype = t[2]

def p_sub_type_3 (t):
    'sub_type : SEQUENCE size_constraint OF type'
    t[0] = Sequence_Of (val = t[4], subtype = t[2])
    
def p_sub_type_4 (t):
    'sub_type : SEQUENCE LPAREN size_constraint RPAREN OF type'
    t[0] = Sequence_Of (val = t[6], subtype = t[3])

def p_subtype_spec_1 (t):
    'subtype_spec : LPAREN subtype_val_set_list RPAREN'
    t[0] = t[2]

def p_subtype_spec_2 (t):
    'subtype_spec : LPAREN subtype_val_set_list COMMA ELLIPSIS RPAREN'
    t[0] = t[2]

def p_subtype_val_set_list_1 (t):
    'subtype_val_set_list : subtype_val_set'
    t[0] = [t[1]]

def p_subtype_val_set_list_2 (t):
    'subtype_val_set_list : subtype_val_set_list BAR subtype_val_set'
    t[0] = t[1] + [t[3]]

def p_subtype_val_set (t):
    '''subtype_val_set : single_value
    | contained_subtype
    | value_range
    | permitted_alphabet
    | size_constraint
    | inner_type_constraints'''
    t[0] = t[1]

def p_single_value (t):
    'single_value : value'
    t[0] = t[1]

def p_contained_subtype (t):
    'contained_subtype : INCLUDES type'
    t[0] = t[2]

def p_value_range (t):
    'value_range : lower_end_point RANGE upper_end_point'
    t[0] = ValueRange(lo=t[1], hi=t[3])

def p_lower_end_point_1 (t):
    'lower_end_point : lower_end_value '
    t[0] = t[1]

def p_lower_end_point_2 (t):
    'lower_end_point : lower_end_value LT' # XXX LT first?
    t[0] = t[1] # but not inclusive range
    
def p_upper_end_point_1 (t):
    'upper_end_point : upper_end_value'
    t[0] = t[1]

def p_upper_end_point_2 (t):
    'upper_end_point : LT upper_end_value'
    t[0] = t[1] # but not inclusive range

def p_lower_end_value (t):
    '''lower_end_value : value
    | MIN'''
    t[0] = t[1] # XXX

def p_upper_end_value (t):
    '''upper_end_value : value
    | MAX'''
    t[0] = t[1]

    
def p_size_constraint (t):
    'size_constraint : SIZE subtype_spec'
    t[0] = Size(subtype = t[2])

def p_permitted_alphabet (t):
    'permitted_alphabet : FROM subtype_spec'
    t[0] = From(subtype = t[2])

def p_inner_type_constraints_1 (t):
    'inner_type_constraints : WITH COMPONENT single_type_constraint'
    t[0] = t[3]

def p_inner_type_constraints_2 (t):
    'inner_type_constraints : WITH COMPONENTS multiple_type_constraints'
    t[0] = t[3]

def p_single_type_constraint (t):
    'single_type_constraint : subtype_spec'
    t[0] = t[1]
#          /* this constrains the elmt of setof or seq of */

def p_multiple_type_constraints (t):
    '''multiple_type_constraints : full_specification
    | partial_specification'''
    t[0] = t[1]

def p_full_specification (t):
    'full_specification : LBRACE type_constraints RBRACE'
    t[0] = t[2]

def p_partial_specification (t):
    'partial_specification : LBRACE ELLIPSIS COMMA type_constraints RBRACE'
    t[0] = t[4]

def p_type_constraints_1 (t):
    'type_constraints : named_constraint'
    t [0] = [t[1]]

def p_type_constraints_2 (t):
    'type_constraints : type_constraints COMMA named_constraint'
    t[0] = t[1] + [t[3]]

def p_named_constraint_1 (t):
    'named_constraint : identifier constraint'
    return Node ('named_constraint', ident = t[1], constr = t[2])

def p_named_constraint_2 (t):
    'named_constraint : constraint'
    return Node ('named_constraint', constr = t[1])

def p_constraint (t):
    'constraint : value_constraint presence_constraint'
    t[0] = Node ('constraint', value = t[1], presence = t[2])

def p_value_constraint_1 (t):
    'value_constraint : subtype_spec'
    t[0] = t[1]

def p_value_constraint_2 (t):
    'value_constraint : '
    pass

def p_presence_constraint_1 (t):
    '''presence_constraint : PRESENT
                 | ABSENT
                 | OPTIONAL'''
    t[0] = t[1]
    
def p_presence_constraint_2 (t):
    '''presence_constraint : '''
    pass

#  /*-----------------------------------------------------------------------*/
#  /* Value Notation Productions */
#  /*-----------------------------------------------------------------------*/


def p_value_assign (t):
    'value_assign : identifier type GETS value'
    return Node ('value_assign', ident = t[1], typ = t[2], val = t[4])

def p_value (t):
    '''value : builtin_value
    | defined_value'''
    t[0] = t[1]

def p_defined_value(t):
    '''defined_value : ext_val_ref
    | identifier'''
    t[0] = t[1]

def p_ext_val_ref (t):
    'ext_val_ref : type_ref DOT identifier'
    # XXX coerce type_ref to module_ref
    return Node ('ext_val_ref', module = t[1], ident = t[3])

def p_builtin_value_1 (t):
    '''builtin_value : boolean_val
    | null_val
    | special_real_val
    | signed_number
    | hex_string
    | binary_string
    | char_string''' # XXX we don't support {data} here
    t[0] = t[1]

def p_boolean_val (t):
    '''boolean_val : TRUE
    | FALSE'''
    t[0] = t[1]

def p_special_real_val (t):
    '''special_real_val : PLUS_INFINITY
    | MINUS_INFINITY'''
    t[0] = t[1]

def p_null_val (t):
    'null_val : NULL'
    t[0] = t[1]

def p_named_value_1 (t):
    'named_value : value'
    t[0] = t[1]

def p_named_value_2 (t):
    'named_value : identifier value'
    t[0] = Node ('named_value', ident = t[1], value = t[2])

def p_oid_val (t):
    'oid_val : LBRACE oid_comp_list RBRACE'
    t[0] = t[2]

def p_oid_comp_list_1 (t):
    'oid_comp_list : oid_comp_list oid_component'
    t[0] = t[1] + [t[2]]

def p_oid_comp_list_2 (t):
    'oid_comp_list : oid_component'
    t[0] = [t[1]]

def p_oid_component (t):
    '''oid_component : number_form
    | name_form
    | name_and_number_form'''
    t[0] = t[1]

def p_number_form (t):
    'number_form : NUMBER'
    t [0] = t[1]

# Note that Z39.50 v3 spec has upper-case here for, e.g., SUTRS.
# I've hacked the grammar to be liberal about what it accepts.
# XXX should have -strict command-line flag to only accept lowercase
# here, since that's what X.208 says.
# XXX I've switched back, because this creates a shift/reduce conflict
# which causes PLY 1.2 and 1.3 to blow up: cope and hack your input files,
# or persuade ITU/ISO/whoever to provide correct specs.

def p_name_form (t):
    '''name_form : type_ref'''
    t[0] = t[1]

def p_name_and_number_form_1 (t):
    '''name_and_number_form : identifier LPAREN number_form RPAREN
    | type_ref LPAREN number_form RPAREN'''
    t[0] = Node ('name_and_number', ident = t[1], number = t[3])

def p_name_and_number_form_2 (t):
    'name_and_number_form : identifier LPAREN defined_value RPAREN'
    t[0] = Node ('name_and_number', ident = t[1], val = t[3])

# see X.208 if you're dubious about lcase only for identifier 
def p_identifier (t):
    'identifier : LCASE_IDENT'
    t[0] = t[1]


def p_binary_string (t):
    'binary_string : BSTRING'
    t[0] = t[1]

def p_hex_string (t):
    'hex_string : HSTRING'
    t[0] = t[1]

def p_char_string (t):
    'char_string : QSTRING'
    t[0] = t[1]

def p_number (t):
    'number : NUMBER'
    t[0] = t[1]


def p_type_ref (t):
    'type_ref : UCASE_IDENT'
    t[0] = Type_Ref (name=t[1])

def p_error(t):
    raise ParseError (str(t))

yacc.yacc ()

# XXX should just calculate dependencies as we go along.  Should be part of prepass, not
# a utility function all back-ends have to call.

def calc_dependencies (node, dict, trace = 0):
    if not hasattr (node, '__dict__'):
        if trace: print("#returning, node=", node)
        return
    if node.type == 'Type_Ref': # XXX
        dict [node.name] = 1
        if trace: print("#Setting", node.name)
        return
    for (a, val) in list(node.__dict__.items ()):
        if trace: print("# Testing node ", node, "attr", a, " val", val)
        if a[0] == '_':
            continue
        elif isinstance (val, type ([])):
            for v in val:
               calc_dependencies (v, dict, trace)
        elif isinstance (val, Node):
            calc_dependencies (val, dict, trace)


def testlex (s, fn, dict):
    lexer.input (s)
    while 1:
        token = lexer.token ()
        if not token:
            break
        print(token)

import sys

if __name__ == '__main__':
    defined_dict = {}
    for fn in sys.argv [1:]:
        f = open (fn, "r")
        ast = yacc.parse (f.read())
        print(list(map (str, ast)))
        lexer.lineno = 1

