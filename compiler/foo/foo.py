#!/usr/bin/env python



"""Compiler from ASN.1 specification to the Python format acceptable
to my asn1.py module.  Loosely based on esnacc grammar.  We ignore
MACROs, CONSUMER INVOKES, SUPPLIER INVOKES, and a lot of stuff, partly
for simplicity and partly because the underlying PLY lexer uses Python
regexps which are limited to 100 named groups in 2.[12] (with, admittedly,
a note: # XXX: <fl> get rid of this limitation!).
It would be possible to either
1) hook in Plex (http://www.cosc.canterbury.ac.nz/~greg/python/Plex/),
which doesn't use Python's re engine
2) Submit a patch to sre.h / _sre.c to dynamically allocate the mark[]
array of SRE_STATE instead of having it be statically declared of SRE_MARK_SIZE.

We also ignore the {...} syntax for basic values, so we don't need separate
lexer states.
"""

class LexError(Exception): pass
class ParseError(Exception): pass

static_tokens = {
#    '\[C\]': 'BOXC',
#    '\[S\]': 'BOXS',
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
                                    'NUMBER']  + list(reserved_words.values ())

def t_OBJECT_IDENTIFIER (t):
    r"OBJECT\s+IDENTIFIER"
    return t

def t_STRING_T(t):
    return t

t_STRING_T.__doc__ = "(%s)String" % "|".join (['(' + x + ')' for x in StringTypes])



import __main__ # XXX blech!

for (k, v) in list(static_tokens.items ()):
    __main__.__dict__['t_' + v] = k

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
    return t

def t_LCASE_IDENT (t):
    r"[a-z](-[a-zA-Z0-9]|[a-zA-Z0-9])*" # can't end w/ '-'
    return t

def t_NUMBER (t):
    r"0|([1-9][0-9]*)"
    return t

def t_COMMENT(t): # XXX want to filter this out entirely, really
    r"--.*\n"
    return None

t_ignore = " \t\r"

def t_NEWLINE(t):
    r'\n+'
    t.lineno += t.value.count("\n")


def t_error(t):
    print("Error", t.value[:100])
    raise LexError

    
import lex
lexer = lex.lex()

import yacc

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
        if hasattr (child, '__getitem__'): #XXX
            return indent + list(map (str, child)) + "\n"
        else:
            return indent + str (child) + "\n"
    def str_depth (self, depth): # ugh
        indent = " " * (4 * depth)
        if hasattr (self.leaf, '__getitem__'):
            lstring = list(map (str, self.leaf))
        else:
            lstring = str (self.leaf)
        l = ["%s%s %s" % (indent, self.type, lstring)]
        l.append ("".join ([self.str_child (s, depth + 1) for s in self.children]))
        return "\n".join (l)
    def __str__(self):
        return "\n" + self.str_depth (0)

def p_module_def (t):
    'module_def : module_ident DEFINITIONS tag_default GETS BEGIN module_body END'
    t[0] = Node ('module', [t[5]], t[1])

def p_tag_default_1 (t):
     '''tag_default : EXPLICIT TAGS
     | IMPLICIT TAGS'''
     t[0] = Node ('tags', leaf = t[1])

def p_tag_default_2 (t):
     'tag_default : '
     t[0] = Node ('tags', leaf = None) # XXX default is EXPLICIT

def p_module_ident (t):
    'module_ident : module_ref assigned_ident' # name, oid
    t [0] = Node ('module_id', [t[1], t[2]])

def p_module_ref (t):
    'module_ref : UCASE_IDENT'
    print("module_ref:", t[1])
    t[0] = t[1]

def p_assigned_ident_1 (t):
    'assigned_ident : oid_val'
    t[0] = t[1]

def p_assigned_ident_2 (t):
    'assigned_ident : '
    pass

def p_module_body_1 (t):
    'module_body : exports imports assign_list'
    t[0] = Node ('module_body', [t[3]])

def p_module_body_2 (t):
    'module_body : '
    t[0] = Node ('module_body')

def p_exports_1 (t):
     'exports : EXPORTS syms_exported SEMICOLON'
     t[0] = Node ('exports', leaf = t[2])

def p_exports_2 (t):
     'exports : '
     pass

def p_syms_exported_1 (t):
     'syms_exported : exp_sym_list'
     t[0] = t[1]

def p_syms_exported_2 (t):
     'syms_exported : '
     pass

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
     pass

def p_syms_imported_1(t):
     'syms_imported : '
     pass

def p_syms_imported_2 (t):
     'syms_imported : syms_from_module_list'
     t[0] = t[1]

def p_syms_from_module_list_1 (t):
     'syms_from_module_list : syms_from_module_list syms_from_module'
     t[0] = t[1] + t[2]

def p_syms_from_module_list_2 (t):
     'syms_from_module_list : syms_from_module'
     t[0] = [t[1]]

def p_syms_from_module (t):
     'syms_from_module : symbol_list FROM module_ident'
     t[0] = Node ('syms_list', [t[1],t[3]])

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
      | value_assign'''
      t[0] = t[1]

def p_type_assign (t):
    'type_assign : type_ref GETS type'
    print("type_assign", t[3], t[1])
    t[0] = Node ('type', [t[3]], t[1])

def p_type (t): # XXX ignore DefinedMacroType
    '''type : builtin_type
    | defined_type
    | sub_type'''
    t[0] = t[1]

def p_ext_type_ref (t):
    'ext_type_ref : module_ref DOT type_ref'
    t[0] = Node ('ext_type_ref', [], (t[1], t[3]))

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
    t[0] = t[1] # XXX


def p_named_type_1 (t):
    'named_type : identifier type'
    t[0] = Node ('named_type', [t[1]], t[2])

def p_named_type_2 (t):
    'named_type : type' # XXX handles selectionType as well old comment??
    t[0] = Node ('named_type', [], t[1])

def p_boolean_type (t):
    'boolean_type : BOOLEAN'
    t[0] = t[1]

def p_integer_type_1 (t):
    'integer_type : INTEGER'
    t[0] = t[1]

def p_integer_type_2 (t):
    'integer_type : INTEGER LBRACE named_number_list RBRACE'
    t[0] = Node ('int_2', [t[3]], t[1])

def p_named_number_list_1 (t):
    'named_number_list : named_number_list COMMA named_number'
    t[0] = t[1] + [t[3]]

def p_named_number_list_2 (t):
    'named_number_list : named_number'
    t[0] = [t[1]]

def p_named_number (t):
    '''named_number : identifier LPAREN signed_number RPAREN
    | identifier LPAREN defined_value RPAREN'''
    t[0] = Node ('named_number', [t[1],t[3]])

# XXX numbers used to errchk for 32-bit ranged
def p_signed_number_1 (t):
    'signed_number : NUMBER'
    t[0] = t [1]

def p_signed_number_2 (t):
    'signed_number : MINUS NUMBER'
    t[0] = -1 * t[1]

def p_enum_type (t):
    'enum_type : ENUMERATED LBRACE named_number_list RBRACE'
    t[0] = Node ('enum', t[3])

def p_real_type (t):
    'real_type : REAL'
    t[0] = t[1]

def p_bitstring_type_1 (t):
    'bitstring_type : BIT STRING'
    t[0] = Node ('bitstring')

def p_bitstring_type_2 (t):
    'bitstring_type : BIT STRING LBRACE named_bit_list RBRACE'
    t[0] = Node ('bitstring', t[4])

def p_named_bit_list (t):
    'named_bit_list : named_number_list'
    t[0] = t[1]

def p_null_type (t):
    'null_type : NULL'
    t[0] = t[1]

def p_sequence_type (t):
    'sequence_type : SEQUENCE LBRACE element_type_list RBRACE'
    t[0] = Node ('sequence', t[3])

def p_element_type_list_1 (t):
    'element_type_list : element_type'
    t[0] = [t[1]]

def p_element_type_list_2 (t):
    'element_type_list : element_type_list COMMA element_type'
    t[0] = t[1] + [t[2]]

def p_element_type_1 (t):
    'element_type : named_type'
    t[0] = Node ('elt_type', [], t[1])

def p_element_type_2 (t):
    'element_type : named_type OPTIONAL'
    t[0] = Node ('elt_type', [t[2]], t[1])

def p_element_type_3 (t):
    'element_type : named_type DEFAULT named_value'
    t[0] = Node ('elt_type', [t[2],t[3]], t[1])
#          /*
#           * this rules uses NamedValue instead of Value
#           * for the stupid choice value syntax (fieldname value)
#           * it should be like a set/seq value (ie with
#           * enclosing { }
#           */

# XXX get to COMPONENTS later, I don't understand it yet

#    | COMPONENTS_SYM OF_SYM Type
#      {
#          $$ = MT (NamedType);
#          SetupType (&$$->type, BASICTYPE_COMPONENTSOF, myLineNoG);
#          $$->type->basicType->a.componentsOf = $3;
#      }
#    | identifier COMPONENTS_SYM OF_SYM Type
#      {
#          $$ = MT (NamedType);
#          SetupType (&$$->type, BASICTYPE_COMPONENTSOF, myLineNoG);
#          $$->fieldName = $1;
#          $$->type->basicType->a.componentsOf = $4;
#      }
#  ;


def p_sequenceof_type (t):
    'sequenceof_type : SEQUENCE OF type'
    print("seq_of:", t[3])
    t[0] = Node ('seq_of', [], t[3])

def p_set_type (t):
    'set_type : SET LBRACE element_type_list RBRACE'
    t[0] = Node ('set', t[3])

def p_setof_type (t):
    'setof_type : SET OF type'
    t[0] = Node ('set_of', [], t[3])

def p_choice_type (t):
    'choice_type : CHOICE LBRACE alternative_type_list RBRACE'
    t[0] = Node ('choice', t[3])

def p_alternative_type_list_1 (t):
    'alternative_type_list : named_type'
    t[0] = [t[1]]

def p_alternative_type_list_2 (t):
    'alternative_type_list : alternative_type_list COMMA named_type'
    t[0] = t[1] + [t[3]]

def p_selection_type (t): # XXX what is this?
    'selection_type : identifier LT type'
    return Node ('seltype', [t[1], t[3]])

def p_tagged_type_1 (t):
    'tagged_type : tag type'
    t[0] = Node ('tag', [t[1],t[2]])
#          /* remove next tag if any  && IMPLICIT_TAGS */
#   	if ((modulePtrG->tagDefault == IMPLICIT_TAGS) &&
#              ($2->tags != NULL) && !LIST_EMPTY ($2->tags))
#          {
#              tag = (Tag*)FIRST_LIST_ELMT ($2->tags); /* set curr to first */
#  	    AsnListFirst ($2->tags); /* set curr to first elmt */
#              AsnListRemove ($2->tags);      /* remove first elmt */

#              /*
#               * set implicit if implicitly tagged built in type (ie not ref)
#               * (this simplifies the module ASN.1 printer (print.c))
#               */
#              if (tag->tclass == UNIV)
#                   $2->implicit = TRUE;

#              Free (tag);
#          }

def p_tagged_type_2 (t):
    'tagged_type : tag IMPLICIT type'
    t[0] = Node ('implicit tag', [t[1],t[3]])
#          /* remove next tag if any */
#   	if (($3->tags != NULL) && !LIST_EMPTY ($3->tags))
#          {
#              tag = (Tag*)FIRST_LIST_ELMT ($3->tags); /* set curr to first */
#  	    AsnListFirst ($3->tags); /* set curr to first elmt */
#              AsnListRemove ($3->tags);      /* remove first elmt */

#              if (tag->tclass == UNIV)
#                   $3->implicit = TRUE;

#              Free (tag);
#          }

#          /*
#           * must check after linking that implicitly tagged
#           * local/import type refs are not untagged choice/any etc
#           */
#          else if (($3->basicType->choiceId == BASICTYPE_IMPORTTYPEREF) ||
#                   ($3->basicType->choiceId == BASICTYPE_LOCALTYPEREF) ||
#                   ($3->basicType->choiceId == BASICTYPE_SELECTION))
#              $3->implicit = TRUE;

#          /*
#           *  all other implicitly tagable types should have tags
#           *  to remove - if this else clause fires then it is
#           *  probably a CHOICE or ANY type
#           */
#          else
#          {
#              PrintErrLoc (modulePtrG->asn1SrcFileName, $3->lineNo);
#              fprintf (stderr, "ERROR - attempt to implicitly reference untagged type\n");
#              smallErrG = 1;
#          }

#          PREPEND ($1, $3->tags);
#          $$ = $3;
#      }


def p_tagged_type_3 (t):
    'tagged_type : tag EXPLICIT type'


def p_tag (t):
    'tag : LBRACK class class_number RBRACK'
    return Node ('tag', [t[2],t[3]])
#          /*
#           *  keep track of APPLICATION Tags per module
#           *  should only be used once
#           */
#          if ($2 == APPL)
#          {
#              PushApplTag ($$->code, myLineNoG);
#          }
#      }
#  ;

def p_class_number_1 (t):
    'class_number : number'
    t[0] = t[1]

def p_class_number_2 (t):
    'class_number : defined_value'
    t[0] = t[1]
#          $$->code = NO_TAG_CODE; # XXX huh?
#          $$->valueRef = $1;


def p_class_1 (t):
    '''class : UNIVERSAL
    | APPLICATION
    | PRIVATE'''
    t[0] = t[1]

def p_class_2 (t):
    '''class : '''
    t[0] = 'CONTEXT' # XXX

def p_any_type_1 (t):
    'any_type : ANY'
    t[0] = Node ('any', [])

def p_any_type_2 (t):
    'any_type : ANY DEFINED BY identifier'
    t[0] = Node ('any', [t[4]])

def p_oid_type (t):
    'oid_type : OBJECT_IDENTIFIER'
    t[0] = t[1]

def p_useful_type (t):
    '''useful_type : GENERALIZEDTIME
    | UTCTIME
    | OBJECTDESCRIPTOR
    | EXTERNAL'''
    t[0] = t[1]

def p_char_str_type (t):
    'char_str_type : STRING_T'
    t[0] = t[1]

def p_sub_type_1 (t):
    'sub_type : type subtype_spec'
    t[0] = Node ('subtype', [t[1],t[2]], '')
#          /*
#           * append new subtype list to existing one (s) if any
#           * with AND relation
#           */
#          AppendSubtype (&$1->subtypes, $2, SUBTYPE_AND);
#          $$ = $1;


def p_sub_type_2 (t):
    'sub_type : SET size_constraint OF type'
    t[0] = Node ('subtype', [t[2],t[4]], 'set')
#          /* add size constraint */
#          s = MT (Subtype);
#          s->choiceId = SUBTYPE_SINGLE;
#          s->a.single = $2;
#          AppendSubtype (&$$->subtypes, s, SUBTYPE_AND);

def p_sub_type_3 (t):
    'sub_type : SEQUENCE size_constraint OF type'
    t[0] = Node ('subtype', [t[2],t[4]], 'seq')

def p_subtype_spec (t):
    'subtype_spec : LPAREN subtype_val_set_list RPAREN'
    t[0] = t[2]

def p_subtype_val_set_list_1 (t):
    'subtype_val_set_list : subtype_val_set'
    t[0] = [t[1]]

def p_subtype_val_set_list_2 (t):
    'subtype_val_set_list : subtype_val_set_list BAR subtype_val_set'
    t[0] = t[1] + t[3]

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
    'value_range : lower_end_point DOT DOT upper_end_point'
    t[0] = [t[1], t[4]]

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
    t[0] = t[2]

def p_permitted_alphabet (t):
    'permitted_alphabet : FROM subtype_spec'
    t[0] = t[2]

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
    'partial_specification : LBRACE DOT DOT DOT COMMA type_constraints RBRACE'
    t[0] = t[6]

def p_type_constraints_1 (t):
    'type_constraints : named_constraint'
    t [0] = [t[1]]

def p_type_constraints_2 (t):
    'type_constraints : type_constraints COMMA named_constraint'
    t[0] = t[1] + t[2]

def p_named_constraint_1 (t):
    'named_constraint : identifier constraint'
    return Node ('named_constraint', [t[1],t[2]])

def p_named_constraint_2 (t):
    'named_constraint : constraint'
    return Node ('named_constraint', [t[1]])

def p_constraint (t):
    'constraint : value_constraint presence_constraint'
    t[0] = Node ('constraint', [t[1], t[2]])

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
    return Node ('value_assign', [t[2],t[4]], t[1])

def p_value (t):
    '''value : builtin_value
    | defined_value'''
    t[0] = t[1]

def p_defined_value(t):
    '''defined_value : ext_val_ref
    | identifier'''
    t[0] = t[1]

def p_ext_val_ref (t):
    'ext_val_ref : module_ref DOT identifier'
    return Node ('ext_val_ref', [t[1],t[3]])

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
    t[0] = Node ('named_value', [t[1],t[2]])
    

def p_oid_val (t):
    'oid_val : LBRACE oid_comp_list RBRACE'
    t[0] = t[2]

def p_oid_comp_list_1 (t):
    'oid_comp_list : oid_comp_list oid_component'
    t[0] = t[1] + t[2] # XXX

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

def p_name_form (t):
    'name_form : identifier'
    t[0] = t[1]


def p_name_and_number_form_1 (t):
    'name_and_number_form : identifier LPAREN number_form RPAREN'
    t[0] = Node ('name_and_number', [t[3]], t[1])

def p_name_and_number_form_2 (t):
    'name_and_number_form : identifier LPAREN defined_value RPAREN'
    t[0] = Node ('name_and_number', [t[3]], t[1])

#Did I make this up?  Weird. XXX
#def p_identifier_1 (t):
#    '''identifier : UCASE_IDENT
#    | LCASE_IDENT'''
#    print "identifier:", t[1]
#    t[0] = t[1]

def p_identifier_2 (t): # XXX!!!
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
    t[0] = t[1]

#  /* Snacc attributes/extra type info
#   *  - encapsulated in special comments
#   */
#  SnaccAttributes:
#      SnaccAttributeCommentList
#    | empty {$$ = NULL;}
#  ;

#  SnaccAttributeCommentList:
#      SNACC_ATTRIBUTES
#      {
#          $$ = NEWLIST();
#          APPEND ($1,$$);
#      }
#    | SnaccAttributeCommentList  SNACC_ATTRIBUTES
#      {
#          APPEND ($2,$1);
#          $$ = $1;
#      }
#  ;



#  OidList:
#      ObjectIdentifierValue
#      {
#          $$ = NEWLIST();
#          APPEND ($1,$$);
#      }
#    | OidList COMMA_SYM ObjectIdentifierValue
#      {
#          APPEND ($3, $1);
#          $$ = $1;
#      }
#  ;


#  /*
#   * MTSAbstractSvc EXTENSIONS macro
#   */

#  MtsasExtensionsMacroType:
#        EXTENSIONS_SYM CHOSEN_SYM FROM_SYM
#        LEFTBRACE_SYM PossiblyEmptyValueList RIGHTBRACE_SYM
#        {
#            MtsasExtensionsMacroType *m;

#            SetupMacroType (&$$, MACROTYPE_MTSASEXTENSIONS, myLineNoG);
#            m = $$->basicType->a.macroType->a.mtsasExtensions =
#                MT (MtsasExtensionsMacroType);
#            m->extensions = $5;
#        }
#  ;


#  PossiblyEmptyValueList:
#      ValueList
#    | empty { $$ = NULL; }
#  ;

#  ValueList:
#       Value
#       {
#           $$ = NEWLIST();
#           APPEND ($1, $$);
#       }
#    | ValueList COMMA_SYM Value
#       {
#           APPEND ($3,$1);
#           $$ = $1;
#       }
#  ;

#  PossiblyEmptyTypeOrValueList:
#      TypeOrValueList
#    | empty { $$ = NULL; }
#  ;

#  TypeOrValueList:
#      TypeOrValue
#       {
#           $$ = NEWLIST();
#           APPEND ($1, $$);
#       }
#    | TypeOrValueList COMMA_SYM TypeOrValue
#       {
#           APPEND ($3,$1);
#           $$ = $1;
#       }
#  ;

#  TypeOrValue:
#      Type
#      {
#           $$ = MT (TypeOrValue);
#           $$->choiceId = TYPEORVALUE_TYPE;
#           $$->a.type = $1;
#       }
#    | Value
#      {
#           $$ = MT (TypeOrValue);
#           $$->choiceId = TYPEORVALUE_VALUE;
#           $$->a.value = $1;
#       }
#  ;


def p_error(t):
    raise ParseError (str(t))

yacc.yacc ()

def testlex (s):
    lexer.input (s)
    while 1:
        token = lexer.token ()
        if not token:
            break
        print(token)
            
def testyacc (s):
    ast = yacc.parse (s)
    assert (ast.type == 'module')
    print("ast:", ast)
#    body = ast.children[0]
#    print "module name:", ast.leaf
#    assignlist = body.children[0]
#    for a in assignlist:
#        print "assign:", a

#    print "AST:", ast

import sys
if __name__ == '__main__':
    testfn = testyacc
    if len (sys.argv) == 1:
        while 1:
            s = input ('Query: ')
            if len (s) == 0:
                break
            testfn (s)
    else:
        for fn in sys.argv [1:]:
            f = open (fn, "r")
            testfn (f.read ())
            f.close ()

