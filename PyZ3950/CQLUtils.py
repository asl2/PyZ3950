
"""Cheshire specific utility functions and subclasses"""

# Lots of faff here that should be cleaned up

from CQLParser import *
from types import ListType, IntType
from SRWDiagnostics import *
# Can we remove this import by checking python version?
from string import  replace, count, join

from PyZ3950 import z3950, asn1, oids
from zcql import ZCQLConfig
zConfig = ZCQLConfig()


class CSearchClause(SearchClause):

    def convertMetachars(self, t):
        "Convert SRW meta characters in to Cheshire's meta characters"
        # Fail on ?, ^ or * not at the end.
        if (count(t, "?") != count(t, "\\?")):
            diag = Diagnostic28()
            diag.details = "? Unsupported"
            raise diag
        elif (count(t, "^") != count(t, "\\^")):
            diag = Diagnostic31()
            diag.details = "^ Unsupported"
            raise diag
        elif (count(t, "*") != count(t, "\\*")):
            if t[-1] != "*" or t[-2] == "\\":
                diag = Diagnostic28()
                diag.details = "Non trailing * unsupported"
                raise diag
            else:
                t[-1] = "#"
        t = replace(t, "\\^", "^")
        t = replace(t, "\\?", "?")
        t = replace(t, "\\*", "*")
        return t

    def toCheshire(self, top=None):
        """ Convert clause into Cheshire search clause """
        # Ugly. Very ugly.

        if top == None:
            top = self

        config = top.config
        if self.relation.value == serverChoiceRelation:
            relation = config.defaultRelation
        else:
            relation = self.relation.value

        idx = convertIndex(self, top)
        if idx  == ":":
            # Pointer to a result set
            return self.term + ":"
        else:
            if idx[0] != "[":
                if relation == "exact":
                    idx = "[bib1 1='%s' 5=100] " % (idx)
                else:
                    idx = "[bib1 1='%s']" % (idx)
            
        if relation == "all":
            # Split term into words and AND together.

            tlist = self.term.split()
            newtlist = []
            for t in tlist:
                newtlist.append(self.convertMetachars(t))
            
            # Relevance?
            clause = "("
            if "relevant" in self.relation.modifiers:
                clause = clause + idx + " @ {" + ''.join(newtlist) + "} AND "
                
            for t in newtlist:
                clause = clause + idx + " {" + t + "} AND "
            clause = clause[:-5]
            clause = clause + ")"

        elif relation == "any":
            # Split term into words and OR together.

            tlist = self.term.split()
            newtlist = []
            for t in tlist:
                newtlist.append(self.convertMetachars(t))
            
            # Relevance?
            if "relevant" in self.relation.modifiers:
                clause = idx + " @ {" + ''.join(newtlist) + "}"
            else:
                clause = "("
                for t in newtlist:
                    clause = clause + idx + " {" + t + "} OR "
                clause = clause[:-4]
                clause = clause + ")"

        elif relation == "=":
            if self.term.isdigit() or not config.useWordIndexes:
                # Numeric
                clause = idx + " = " + self.term
            else:
                # Adjacent:  fooWord = {$term$}
                clause = idx + " = {$" + self.term + "$}"


                if "relevant" in self.relation.modifiers:
                    clause = "(" + clause + " AND " + idx + " @ {" + self.term + "})"
        elif relation == "exact":
            clause = idx + " " + self.term
        elif relation in ['>', '<', '>=', '<=', '<>']:
            clause = idx + " " + relation + " {" + self.term + "}"
        else:
            # Uhoh!
            raise(ValueError)

        return clause

    def toRPN(self):
        if (self.relation.value in ['any', 'all']):
            # Need to split this into and/or tree
            if (self.relation.value == 'any'):
                bool = " or "
            else:
                bool = " and "
            words = self.term.value.split()
            self.relation.value = '='
            # Add 'word' relationModifier
            self.relation.modifiers.append(CModifierClause('cql.word'))
            
            # Create CQL, parse it, walk new tree
            idxrel = "%s %s" % (self.index.toCQL(), self.relation.toCQL())
            text = []
            for w in words:
                text.append('%s "%s"' % (idxrel, w))
            cql = bool.join(text)
            tree = parse(cql)
            return tree.toRPN()
        else:
            # attributes, term
            # AttributeElement: attributeType, attributeValue
            # attributeValue ('numeric', n) or ('complex', struct)
            clause = z3950.AttributesPlusTerm()

            attrs = [self.index.toRPN()]
            if (self.term.value.isdigit()):
                self.relation.modifiers.append(CModifierClause('cql.number'))
            attrs.extend(self.relation.toRPN())

            def make_attr(a):
                ae = z3950.AttributeElement()
                ae.attributeType = a[0]
                if (type(a[1]) == IntType):
                    ae.attributeValue = ('numeric', a[1])
                else:
                    cattr = z3950.AttributeElement['attributeValue']['complex']()
                    cattr.list = [('string', a[1])]
                    ae.attributeValue = ('complex', cattr)
                return ae

            clause.attributes = map(make_attr, attrs)
            clause.term = self.term.toRPN()

            return ('op', ('attrTerm', clause))


class CBoolean(Boolean):
    def toCheshire(self):
        """ Convert boolean into Cheshire  """
        if self.modifiers:
            # Proximity
            # ! [O]NEAR (<) [O]FAR (>)  / Unit / Distance
            if self.modifiers[0] in ['>', '>=']:
                prox = "FAR"
            else:
                prox = "NEAR"
            if self.modifiers[3] == 'ordered':
                prox = "O" + prox
            prox = "!" + prox
            if self.modifiers[2] == '':
                prox = prox + "/WORD"
            else:
                prox = prox + "/" + self.modifiers[2]
            if self.modifiers[1] != '':
                prox = prox + "/" + str(self.modifiers[1])
            elif self.modifiers[2] in ['', 'word']:
                # Default distance is 1
                prox = prox + "/1"
            else:
                prox = prox + "/0"

            return " " + prox + " "
        else:
            return " " + self.value + " "

    def toRPN(self):
        op = self.value
        if (self.value == 'not'):
            op = 'and-not'
        elif (self.value == 'prox'):
            # Create ProximityOperator
            prox = z3950.ProximityOperator()
            # distance, ordered, proximityUnitCode, relationType
            u = self['unit']
            try:
                units = ["", "character", "word", "sentence", "paragraph", "section", "chapter", "document", "element", "subelement", "elementType", "byte"]
                if (u.value in units):
                    prox.unit = ('known', units.index(u.value))
                else:
                    # Uhhhh.....
                    prox.unit = ('private', int(u.value))
            except:
                prox.unit = ('known', 2)

            d = self['distance']
            try:
                prox.distance = int(d.value)
            except:
                if (prox.unit == ('known', 2)):
                    prox.distance = 1
                else:
                    prox.distance = 0
            try:
                rels = ["", "<", "<=", "=", ">=", ">", "<>"]
                prox.relationType = rels.index(d.comparison)
            except:
                prox.relationType = 2

            prox.ordered = bool(self['ordered'])
            return ('op', ('prox', prox))
                    
        return (op, None)
    
class CTriple(Triple):

    def toCheshire(self, top=None):
        """ Convert triple into Cheshire search clause """
        if top == None:
            top = self
        string = "(" + self.leftOperand.toCheshire(top) + self.boolean.toCheshire() + self.rightOperand.toCheshire(top) + ")"
        return string

    def toRPN(self):
        """rpnRpnOp"""
        op = z3950.RpnRpnOp()
        op.rpn1 = self.leftOperand.toRPN()
        op.rpn2 = self.rightOperand.toRPN()
        op.op = self.boolean.toRPN()
        return op


class CIndex(Index):
    def toRPN(self):
        pf = self.prefix
        if (not pf or pf in ['cql', 'dc']):
            pf = "bib1"
        pf = pf.upper()
        try:
            set = oids.oids['Z3950']['ATTRS'][pf]['oid']
        except:
            # Can't generate the set ...
            raise(ValueError)
        
        if (self.value.isdigit()):
            # bib1.1018
            val = int(self.value)
        elif (hasattr(zConfig, pf)):
            map = getattr(zConfig, pf)
            if (map.has_key(self.value)):
                val = map[self.value]
            else:
                val = self.value
        else:
            # complex attribute for bib1
            val = self.value
            
        return (1, val)
            

class CRelation(Relation):
    def toRPN(self):
        rels = ['', '<', '<=', '=', '>=', '>', '<>']

        vals = [None, None, None, None, None, None, None]

        if self.value in rels:
            vals[2] = rels.index(self.value)
        elif self.value in ['exact', 'scr']:
            vals[2] = 3
        elif (self.value == 'within'):
            vals[2] = 104

        if self['relevant']:
            vals[2] = 102
        elif self['stem']:
            vals[2] = 101
        elif self['phonetic']:
            vals[2] = 100

        if self['number']:
            vals[4] = 109
            vals[5] = 100
        elif self['date']:
            vals[4] = 5
        elif self['word']:
            vals[4] = 2

        if self.value == 'exact':
            vals[3] = 1
            vals[5] = 100 
            vals[6] = 3
        else:
            vals[3] = 3
            vals[6] = 1

        attrs = []
        for x in range(1,7):
            if vals[x]:
                attrs.append((x, vals[x]))

        return attrs
        

class CTerm(Term):
    def toRPN(self):
        return ('general', self.value)

class CModifierClause(ModifierClause):
    pass

class CModifierType(ModifierType):
    pass


def convertIndex(sc, top):
    "Convert srw indexset.index into Cheshire index name"
    idx = sc.index
    config = top.config
    cql = config.contextSetNamespaces['cql']

    idx.resolvePrefix()
    
    if idx.prefixURI == cql and idx.value == "serverchoice":
        index = config.defaultIndex
        set = config.defaultContextSet

    if idx.prefixURI == cql and idx.value == "resultsetname":
        return ":"

    if config.indexHash.has_key(set) and config.indexHash[set].has_key(idx):
        idx = config.indexHash[set][idx]

    if type(idx) == ListType:

        # Need to mung for Word type and Exact
        if (sc.relation.value == "exact" and not ['bib1', 5, 100] in idx):
            idx.append(['bib1', 5, 100])

        if (sc.relation.value in ['all', 'any', 'scr'] or (sc.relation.value == '=' and (not sc.term.isdigit() or sc.relation.modifiers))):
            # Word style.
            for a in range(len(idx)):
                if idx[a][1] == "3":
                    idx[a][2] = "3"
                elif idx[a][1] == "4":
                    idx[a][2] = "6"
        # Now convert to string
        idxList = ["["]
        for i in idx:
            idxList.append("%s %s=%s, " % (i[0], i[1], i[2]))
        idx = ''.join(idxList)[:-2] + "]"
        return idx
                                                          
    else:
        if config.useWordIndexes and idx[-4:] != "Word":
            if sc.relation.value in ['all', 'any', 'scr']:
                idx = idx + "Word"
            if sc.relation.value == "=" and (not sc.term.isdigit() or sc.relation.modifiers):
                idx = idx + "Word"
            if "stem" in sc.relation.modifiers:
                idx = idx + "Stem"

    return idx


