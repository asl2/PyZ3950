#!/usr/local/bin/python2.3

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from PyZ3950 import z3950, oids
from PyZ3950.zdefs import make_attr
from types import IntType, StringType, ListType
# We need "\"\""  to be one token
from CQLParser import CQLshlex


"""
Parser for PQF directly into RPN structure.
PQF docs: http://www.indexdata.dk/yaz/doc/tools.html
"""


class PQFParser:
    lexer = None
    currentToken = None
    nextToken = None

    def __init__(self, l):
        self.lexer = l
        self.fetch_token()

    def fetch_token(self):
        """ Read ahead one token """
        tok = self.lexer.get_token()
        self.currentToken = self.nextToken
        self.nextToken = tok

    def is_boolean(self):
        if (self.currentToken.lower() in ['@and', '@or', '@not', '@prox']):
            return True
        else:
            return False

    def defaultClause(self, t):
        # Assign a default clause: anywhere =
        clause = z3950.AttributesPlusTerm()
        attrs = [(oids.Z3950_ATTRS_BIB1, 1, 1016), (oids.Z3950_ATTRS_BIB1, 2, 3)]
        clause.attributes = [make_attr(*e) for e in attrs]
        clause.term = t
        return ('op', ('attrTerm', clause))

    #  Grammar fns

    def query(self):
        set = self.top_set()
        qst = self.query_struct()

        # Pull in a (hopefully) null token
        self.fetch_token()
        if (self.currentToken):
            # Nope, unprocessed tokens remain
            raise(ValueError)

        rpnq = z3950.RPNQuery()
        if set:
            rpnq.attributeSet = set
        else:
            rpnq.attributeSet = oids.Z3950_ATTRS_BIB1_ov
        rpnq.rpn = qst


        return ('type_1', rpnq)

    def top_set(self):
        if (self.nextToken == '@attrset'):
            self.fetch_token()
            self.fetch_token()
            n = self.currentToken.upper()
            # Will raise KeyError if not exist
            return oids.oids['Z3950']['ATTRS'][n]['oid']
        else:
            return None

    # This totally ignores the BNF, but does the 'right' thing
    def query_struct(self):
        self.fetch_token()
        if (self.currentToken == '@attr'):
            attrs = []
            while self.currentToken == '@attr':
                attrs.append(self.attr_spec())
                self.fetch_token()
            t = self.term()

            # Now we have attrs + term
            clause = z3950.AttributesPlusTerm()
            clause.attributes = [make_attr(*e) for e in attrs]
            clause.term = t
            return ('op', ('attrTerm', clause))
        elif (self.is_boolean()):
            # @operator query query
            return self.complex()
        elif (self.currentToken == '@set'):
            return self.result_set()
        elif (self.currentToken == "{"):
            # Parens
            s = self.query_struct()
            if (self.nextToken <> "}"):
                raise(ValueError)
            else:
                self.fetch_token()
            return s
            
        else:
            t = self.term()
            return self.defaultClause(t)

    def term(self):
        # Need to split to allow attrlist then @term
        type = 'general'
        if (self.currentToken == '@term'):
            self.fetch_token()
            type = self.currentToken.lower()
            types = {'general' : 'general', 'string' : 'characterString', 'numeric' : 'numeric', 'external' : 'external'}
            type = types[type]
            self.fetch_token()

        if (self.currentToken[0] == '"' and self.currentToken[-1] == '"'):
            term = self.currentToken[1:-1]
        else:
            term = self.currentToken

        return (type, term)
            
    def result_set(self):
        self.fetch_token()
        return ('op', ('resultSet', self.currentToken))

    def attr_spec(self):
        # @attr is CT
        self.fetch_token()
        if (not self.currentToken[0].isdigit()):
            # attrset
            set = self.currentToken
            set = oids.oids['Z3950']['ATTRS'][set.upper()]['oid']
            self.fetch_token()
        else:
            set = None
        # May raise
        (atype, val) = self.currentToken.split('=')
        if (not atype.isdigit()):
            raise ValueError
        atype = int(atype)
        if (val.isdigit()):
            val = int(val)
        return (set, atype, val)

    def complex(self):
        op = z3950.RpnRpnOp()
        op.op = self.boolean()
        op.rpn1 = self.query_struct()
        op.rpn2 = self.query_struct()
        return ('rpnRpnOp', op)

    def boolean(self):
        b = self.currentToken[1:]
        b = b.lower()
        if (b == 'prox'):
            self.fetch_token()
            exclusion = self.currentToken
            self.fetch_token()
            distance = self.currentToken
            self.fetch_token()
            ordered = self.currentToken
            self.fetch_token()
            relation = self.currentToken
            self.fetch_token()
            which = self.currentToken
            self.fetch_token()
            unit = self.currentToken

            prox = z3950.ProximityOperator()
            if (not (relation.isdigit() and exclusion.isdigit() and distance.isdigit() and unit.isdigit())):
                raise ValueError
            prox.relationType = int(relation)
            prox.exclusion = bool(exclusion)
            prox.distance = int(distance)
            if (which[0] == 'k'):
                prox.unit = ('known', int(unit))
            elif (which[0] == 'p'):
                prox.unit = ('private', int(unit))
            else:
                raise ValueError

            return (b, prox)
        elif b == 'not':
            return ('and-not', None)
        else:
            return (b, None)
            

def parse(q):

    query = StringIO(q)
    lexer = CQLshlex(query)
    # Override CQL's wordchars list to include /=><()
    lexer.wordchars += "!@#$%^&*-+[];,.?|~`:\\><=/'()"
    
    parser = PQFParser(lexer)
    return parser.query()



