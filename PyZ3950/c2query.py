
#!/usr/local/bin/python2.3

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from PyZ3950 import z3950, oids
from types import IntType, StringType, ListType
# We need "\"\""  to be one token
from PyZ3950.CQLParser import CQLshlex
from PyZ3950.CQLUtils import ZCQLConfig
from PyZ3950.zdefs import make_attr
zconfig = ZCQLConfig()

"""
http://cheshire.berkeley.edu/cheshire2.html#zfind

top        ::= query ['resultsetid' name]
query      ::= query boolean clause | clause 
clause     ::=  '(' query ')'
               | attributes [relation] term
               | resultset
attributes ::= '[' { [set] type '=' value } ']' | name
boolean    ::= 'and' | 'or' | 'not' | (synonyms)
prox       ::= ('!PROX' | (synonyms)) {'/' name}
relation   ::= '>' | '<' | ...

[bib1 1=5, bib1 3=6] > term and title @ fish
"""

booleans = {'AND' : 'and',
            '.AND.' : 'and',
            '&&' : 'and',
            'OR' : 'or',
            '.OR.' : 'or',
            '||' : 'or',
            'NOT' : 'and-not',
            '.NOT.' : 'and-not',
            'ANDNOT' : 'and-not',
            '.ANDNOT.' : 'and-not',
            '!!' : 'and-not'
            }

relations = {'<' : 1,
             'LT' : 1,
             '.LT.' : 1,
             '<=' : 2,
             'LE' : 2,
             '.LE.' : 2,
             '=' : 3,
             '>=' : 4,
             'GE' : 4,
             '.GE.' : 4,
             '>' : 5,
             'GT' : 5,
             '.GT.' : 5,
             '<>' : 6,
             '!=' : 6,
             'NE' : 6,
             '.NE.' : 6,
             '?' : 100,
             'PHON' : 100,
             '.PHON.' : 100,
             '%' : 101,
             'STEM' : 101,
             '.STEM.' : 101,
             '@' : 102,
             'REL' : 102,
             '.REL.' : 102,
             '<=>' : 104,
             'WITHIN' : 104,
             '.WITHIN.' : 104}

geoRelations = {'>=<' : 7,
                '.OVERLAPS.' : 7,
                '>#<' : 8,
                '.FULLY_ENCLOSED_WITHIN.' : 8,
                '<#>' : 9,
                '.ENCLOSES.' : 9,
                '<>#' : 10,
                '.OUTSIDE_OF.' : 10,
                '+-+' : 11,
                '.NEAR.' : 11,
                '.#.' : 12,
                '.MEMBERS_CONTAIN.' : 12,
                '!.#.' : 13,
                '.MEMBERS_NOT_CONTAIN.' : 13,
                ':<:' : 14,
                '.BEFORE.' : 14,
                ':<=:' : 15,
                '.BEFORE_OR_DURING.' : 15,
                ':=:' : 16,
                '.DURING.' : 16,
                ':>=:' : 17,
                '.DURING_OR_AFTER.' : 17,
                ':>:' : 18,
                '.AFTER.' : 18}

proxBooleans = {'!PROX' : (2, 0, 2),
                '!ADJ' : (2, 0, 2),
                '!NEAR' : (20, 0, 2),
                '!FAR' : (20, 0, 4),
                '!OPROX' : (2, 1, 2),
                '!OADJ' : (2, 1, 2),
                '!ONEAR' : (20, 1, 2),
                '!OFAR' : (20, 1, 4)}

proxUnits = {'C' : 1,
             'CHAR' : 1,
             'W' : 2,
             'WORD' : 2,
             'S' : 3,
             'SENT' : 3,
             'SENTENCE' : 3,
             'P' : 4,
             'PARA' : 4,
             'PARAGRAPH' : 4,
             'SECTION' : 5,
             'CHAPTER' : 6,
             'DOCUMENT' : 7,
             'ELEMENT' : 8,
             'SUBELEMENT' : 9,
             'ELEMENTTYPE' : 10,
             'BYTE' : 11}

privateBooleans = {'!FUZZY_AND' : 1,
                   '!FUZZY_OR' : 2,
                   '!FUZZY_NOT' : 3,
                   '!RESTRICT_FROM' : 4,
                   '!RESTRICT_TO' : 5,
                   '!MERGE_SUM' : 6,
                   '!MERGE_MEAN' : 7,
                   '!MERGE_NORM' : 8}
                   
xzconfig = ZCQLConfig()

class C2Parser:
    lexer = None
    currentToken = None
    nextToken = None

    def __init__(self, l):
        self.lexer = l
        self.fetch_token()


    def fetch_token(self):
        tok = self.lexer.get_token()
        self.currentToken = self.nextToken
        self.nextToken = tok

    def is_boolean(self, tok=None):
        if (tok == None):
            tok = self.currentToken
        if (privateBooleans.has_key(tok.upper())):
            return 1
        elif (booleans.has_key(tok.upper())):
            return 2
        elif (proxBooleans.has_key(tok.upper())):
            return 3
        else:
            return 0


    def top(self):

        rpn = self.query()
        # Check for resultsetid
        if (self.currentToken.lower() == 'resultsetid'):
            self.fetch_token()
            resultset = self.currentToken
        else:
            resultset = None

        rpnq = z3950.RPNQuery()
        rpnq.attributeSet = oids.Z3950_ATTRS_BIB1_ov
        rpnq.rpn = rpn
        q = ('type_1', rpnq)
        return (q, resultset)

    def query(self):
        self.fetch_token()
        left = self.subquery()
        while 1:
            if not self.currentToken:
                break
            bool = self.is_boolean()
            if bool:
                bool = self.boolean()
                right = self.subquery()
                # Put left into triple, make triple new left
                op = z3950.RpnRpnOp()
                op.rpn1 = left
                op.rpn2 = right
                op.op = bool
                wrap = ('rpnRpnOp', op)
                left = wrap
            else:
                break
        return left

            
    def subquery(self):
        if self.currentToken == "(":
            object = self.query()
            if (self.currentToken <> ")"):
                raise ValueError
            else:
                self.fetch_token()
        else:
            object = self.clause()
        return object

    def boolean(self):
        tok = self.currentToken.upper()
        self.fetch_token()
        if (booleans.has_key(tok)):
            return (booleans[tok], None)
        elif (privateBooleans.has_key(tok)):
            # Generate cutesie prox trick
            type = privateBooleans[tok]
            prox = z3950.ProximityOperator()
            prox.proximityUnitCode = ('private', type)
            prox.distance = 0
            prox.ordered = 0
            prox.relationType = 3
            return ('op', ('prox', prox))

        elif (proxBooleans.has_key(tok)):
            # Generate prox
            prox = z3950.ProximityOperator()
            stuff = proxBooleans[tok]
            prox.distance = stuff[0]
            prox.ordered = stuff[1]
            prox.relationType = stuff[2]
            prox.proximityUnitCode = ('known', 2)

            # Now look for /
            while (self.currentToken == "/"):
                self.fetch_token()
                if (self.currentToken.isdigit()):
                    prox.distance = int(self.currentToken)
                elif (proxUnits.has_key(self.currentToken.upper())):
                    prox.proximityUnitCode = ('known', proxUnits[self.currentToken.upper()])
                else:
                    raise ValueError
                self.fetch_token()
            return ('op', ('prox', prox))
        else:
            # Argh!
            raise ValueError
        
    def clause(self):

        if (self.is_boolean(self.nextToken) or not self.nextToken or self.nextToken.lower() == 'resultsetid' or self.nextToken == ")"):
            # Must be a resultset
            tok = self.currentToken
            self.fetch_token()
            return ('op', ('resultSet', tok))

        elif (self.currentToken == '['):
            # List of attributes
            attrs = []
            oidHash = oids.oids['Z3950']['ATTRS']
            while (1):
                self.fetch_token()

                if (self.currentToken == ']'):
                    break

                if (oidHash.has_key(self.currentToken)):
                    attrSet = oidHash[self.currentToken]['ov']
                    self.fetch_token()
                elif (self.currentToken[:8] == '1.2.840.'):
                    attrSet = asn1.OidVal(map(int, self.currentToken.split('.')))
                    self.fetch_token()
                else:
                    attrSet = None

                if (self.currentToken[-1] == ','):
                    tok = self.currentToken[:-1]
                else:
                    tok = self.currentToken

                if (tok.isdigit()):
                    # 1 = foo
                    atype = int(tok)
                    self.fetch_token()
                    if (self.currentToken == '='):
                        # = foo
                        self.fetch_token()

                    if (self.currentToken[0] == '='):
                        # =foo
                        tok = self.currentToken[1:]
                    else:
                        tok = self.currentToken

                    if (tok[-1] == ','):
                        tok = tok[:-1]

                    if (tok.isdigit()):
                        val = int(tok)
                    else:
                        val = tok
                        if (val[0] == "'" and val[-1] == "'"):
                            val = val[1:-1]
                elif (tok[-1] == '='):
                    #1= foo
                    tok = tok[:-1]
                    if (tok.isdigit()):
                        atype = int(tok)
                    self.fetch_token()
                    if (self.currentToken[-1] == ","):
                        tok = self.currentToken[:-1]
                    else:
                        tok = self.currentToken
                    if (tok.isdigit()):
                        val = int(self.currentToken)
                    else:
                        val = tok
                        if (val[0] == "'" and val[-1] == "'"):
                            val = val[1:-1]

                elif (tok.find('=') > -1):
                    # 1=foo
                    (atype, val) = self.currentToken.split('=')
                    atype = int(atype)
                    if (val[-1] == ","):
                        val = val[:-1]
                    if (val.isdigit()):
                        val = int(val)
                    elif (val[0] == "'" and val[-1] == "'"):
                        val = val[1:-1]
                else:
                    # ???
                    raise ValueError
                attrs.append([attrSet, atype, val])

        else:
            # Check for named index
            if (zconfig.BIB1.has_key(self.currentToken.lower())):
                attrs = [[oids.Z3950_ATTRS_BIB1_ov, 1, zconfig.BIB1[self.currentToken.lower()]]]
            else:
                # Just pass through the name
                attrs = [[oids.Z3950_ATTRS_BIB1_ov, 1, self.currentToken]]

        self.fetch_token()
        # Check for relation
        tok = self.currentToken.upper()
        if (relations.has_key(tok)):
            val = relations[tok]
            found = 0
            for a in attrs:
                if (a[0] in [oids.Z3950_ATTRS_BIB1, None] and a[1] == 2):
                    found =1 
                    a[2] = val
                    break
            if (not found):
                attrs.append([None, 2, val])
            self.fetch_token()
        elif (geoRelations.has_key(tok)):
            val = geoRelations[tok]
            found = 0
            for a in attrs:
                if (a[0] in [oids.Z3950_ATTRS_BIB1, oids.Z3950_ATTRS_GEO, None] and a[1] == 2):
                    found = 1
                    a[2] = val
                    break
            if (not found):
                attrs.append([oids.Z3950_ATTRS_GEO, 2, val])
            self.fetch_token()

        if (self.currentToken.find(' ')):
            # Already quoted
            term = self.currentToken
        else:
            # Accumulate
            term = []
            while (self.currentToken and not self.is_boolean(self.currentToken) and self.currentToken.lower() != 'resultsetid'):
                term.append(self.currenToken)
            term = ' '.join(term)

        self.fetch_token()
            
        # Phew. Now build AttributesPlusTerm
        clause = z3950.AttributesPlusTerm()
        clause.attributes = [make_attr(*e) for e in attrs]
        clause.term = ('general', term)
        return ('op', ('attrTerm', clause))


def parse(q):

    query = StringIO(q)
    lexer = CQLshlex(query)
    # Override CQL's wordchars list to include /=><
    lexer.wordchars += "!@#$%^&*-+;,.?|~`:\\><='"
    lexer.wordchars = lexer.wordchars.replace('[', '')
    lexer.wordchars = lexer.wordchars.replace(']', '')
    
    
    parser = C2Parser(lexer)
    return parser.top()

