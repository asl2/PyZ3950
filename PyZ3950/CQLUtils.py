
"""CQL utility functions and subclasses"""

from CQLParser import *
from types import ListType, IntType
from SRWDiagnostics import *

from PyZ3950 import z3950, asn1, oids
from PyZ3950.zdefs import make_attr

asn1.register_oid (oids.Z3950_QUERY_CQL, asn1.GeneralString)

class ZCQLConfig:

    contextSets = {'dc' : 'info:srw/cql-context-set/1/dc-v1.1',
                   'cql' : 'info:srw/cql-context-set/1/cql-v1.1',
                   'bath' : 'http://zing.z3950.org/cql/bath/2.0/',
                   'zthes' : 'http://zthes.z3950.org/cql/1.0/', 
                   'ccg' : 'http://srw.cheshire3.org/contextSets/ccg/1.1/ ',
                   'rec' : 'info:srw/cql-context-set/2/rec-1.0',
                   'net' : 'info:srw/cql-context-set/2/net-1.0'}

    dc = {'title' : 4,
          'subject' : 21,
          'creator' : 1003,
          'author' : 1003,
          'editor' : 1020,
          'contributor' : 1018,
          'publisher' : 1018,
          'description' : 62,
          'date' : 30,
          'resourceType' : 1031,
          'type' : 1031,
          'format' : 1034,
          'identifier' : 12,
          'source' : 1019,
          'language' : 54,
          'relation' : 1016,
          'coverage' : 1016,
          'rights' : 1016
          }

    cql = {'anywhere' : 1016,
           'serverChoice' : 1016}

    # The common bib1 points
    bib1 = {"personal_name" : 1,
            "corporate_name" : 2,
            "conference_name" : 3,
            "title" : 4,
            "title_series" : 5,
            "title_uniform" : 6,
            "isbn" : 7,
            "issn" : 8,
            "lccn" : 9,
            "local_number" : 12,
            "dewey_number" : 13,
            "lccn" : 16,
            "local_classification" : 20,
            "subject" : 21,
            "subject_lc" : 27,
            "subject_local" : 29,
            "date" : 30,
            "date_publication" : 31,
            "date_acquisition" : 32,
            "local_call_number" : 53,
            "abstract" : 62,
            "note" : 63,
            "record_type" : 1001,
            "name" : 1002,
            "author" : 1003,
            "author_personal" : 1004,
            "identifier" : 1007,
            "text_body" : 1010,
            "date_modified" : 1012,
            "date_added" : 1011,
            "concept_text" : 1014,
            "any" : 1016,
            "default" : 1017,
            "publisher" : 1018,
            "record_source" : 1019,
            "editor" : 1020,
            "docid" : 1032,
            "anywhere" : 1035,
            "sici" : 1037
            }

    exp1 = {"explainCategory" :1,
            "humanStringLanguage" : 2,
            "databaseName" : 3,
            "serverName" : 4,
            "attributeSetOID" : 5,
            "recordSyntaxOID" : 6,
            "tagSetOID" : 7,
            "extendedServiceOID" : 8,
            "dateAdded" : 9,
            "dateChanged" : 10,
            "dateExpires" : 11,
            "elementSetName" : 12,
            "processingContext" : 13,
            "processingName" : 14,
            "termListName" : 15,
            "schemaOID" : 16,
            "producer" : 17,
            "supplier" : 18,
            "availability" : 19,
            "proprietary" : 20,
            "userFee" : 21,
            "variantSetOID" : 22,
            "unitSystem" : 23,
            "keyword" : 24,
            "explainDatabase" : 25,
            "processingOID" : 26
            }
  
    xd1 = {"title" : 1,
          "subject" : 2,
          "name" : 3,
          "description" : 4,
          "date" : 5,
          "type" : 6,
          "format" : 7,
          "identifier" : 8,
          "source" : 9,
          "langauge" : 10,
          "relation" : 11,
          "coverage" : 12,
          "rights" : 13}

    util = {"record_date" : 1,
            "record_agent" : 2,
            "record_language" : 3,
            "control_number" : 4,
            "cost" : 5,
            "record_syntax" : 6,
            "database_schema" : 7,
            "score" : 8,
            "rank" : 9,
            "result_set_position" : 10,
            "all" : 11,
            "anywhere" : 12,
            "server_choice" : 13,
            "wildcard" : 14,
            "wildpath" : 15}

    defaultAttrSet = z3950.Z3950_ATTRS_BIB1_ov

    def __init__(self):
        self.util1 = self.util
        self.xd = self.xd1

    def attrsToCql(self, attrs):
        hash = {}
        for c in attrs:
            if (not c[0]):
                c[0] = self.defaultAttrSet
            hash[(c[0], c[1])] = c[2]
        bib1 = z3950.Z3950_ATTRS_BIB1_ov
        use = hash.get((bib1, 1), 4)
        rel = hash.get((bib1, 2), 3)
        posn = hash.get((bib1, 3), None)
        struct = hash.get((bib1, 4), None)
        trunc = hash.get((bib1, 5), None)
        comp = hash.get((bib1, 6), None)

        index = None
        if (not isinstance(use, int)):
            index = indexType(use)
        else:
            for v in self.dc.items():
                if use == v[1]:
                    index = indexType("dc.%s" % (v[0]))
                    break
            if not index:
                for v in self.bib1.items():
                    if (use == v[1]):
                        index = indexType("bib1.%s" % (v[0]))
                        break
            if not index:
                    index  = indexType("bib1.%i" % (use))

        relations = ['', '<', '<=', '=', '>=', '>', '<>']
        if (comp == 3):
            relation = relationType("exact")
        elif (rel > 6):
            if struct in [2, 6]:
                relation = relationType('any')
            else:
                relation = relationType('=')
        else:
            relation = relationType(relations[rel])

        if (rel == 100):
            relation.modifiers.append(modifierClauseType('phonetic'))
        elif (rel == 101):
            relation.modifiers.append(modifierClauseType('stem'))
        elif (rel == 102):
            relation.modifiers.append(modifierClauseType('relevant'))

        if (struct in [2, 6]):
            relation.modifiers.append(modifierClauseType('word'))
        elif (struct in [4, 5, 100]):
            relation.modifiers.append(modifierClauseType('date'))
        elif (struct == 109):
            relation.modifiers.append(modifierClauseType('number'))
        elif (struct in [1, 108]):
            relation.modifiers.append(modifierClauseType('string'))
        elif (struct == 104):
            relation.modifiers.append(modifierClauseType('uri'))
            
        return (index, relation)

zConfig = ZCQLConfig()

def rpn2cql(rpn, config=zConfig, attrSet=None):
    if rpn[0] == 'op':
        # single search clause
        op = rpn[1]
        type = op[0]
        if type == 'attrTerm':
            attrs = op[1].attributes
            term = op[1].term
            combs = []
            for comb in attrs:
                if hasattr(comb, 'attributeSet'):
                    attrSet = comb.attributeSet
                if hasattr(comb, 'attributeType'):
                    aType = comb.attributeType
                else:
                    # Broken!
                    aType = 1
                vstruct = comb.attributeValue
                if (vstruct[0] == 'numeric'):
                    aValue = vstruct[1]
                else:
                    # Complex attr value
                    vstruct = vstruct[1]
                    if (hasattr(vstruct, 'list')):
                        aValue = vstruct.list[0][1]
                    else:
                        # semanticAction?
                        aValue = vstruct.semanticAction[0][1]
                combs.append([attrSet, aType, aValue])
            # Now let config do its thing
            (index, relation) = config.attrsToCql(combs)
            return searchClauseType(index, relation, termType(term[1]))

        elif type == 'resultSet':
            return searchClauseType(indexType('cql.resultSetId'), relationType('='), termType(op[0]))

    elif rpn[0] == 'rpnRpnOp':
        triple = rpn[1]
        bool = triple.op
        lhs = triple.rpn1
        rhs = triple.rpn2
        ctrip = tripleType()
        ctrip.leftOperation = rpn2cql(lhs, config)
        ctrip.rightOperand = rpn2cql(rhs, config)
        ctrip.boolean = booleanType(bool[0])
        if bool[0] == 'prox':
            distance = bool[1].distance
            order = bool[1].ordered
            if order:
                order = "ordered"
            else:
                order = "unordered"
            relation = bool[1].relationType
            rels = ["", "<", "<=", "=", ">=", ">", "<>"]
            relation = rels[relation]
            unit = bool[1].proximityUnitCode
            units = ["", "character", "word", "sentence", "paragraph", "section", "chapter", "document", "element", "subelement", "elementType", "byte"]
            if unit[0] == "known":
                unit = units[unit[1]]
            mods = [cql.modifierClauseType('distance', relation, str(distance)), cql.modifierClauseType('word', '=', unit), cql.modifierClauseType(order)]
            ctrip.boolean.modifiers = mods
        return ctrip

    elif rpn[0] == 'type_1':
        q = rpn[1]
        return rpn2cql(q.rpn, config, q.attributeSet)
    



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

    def toRPN(self, top=None):
        if not top:
            top = self

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
            tree.prefixes = self.prefixes
            tree.parent = self.parent
            tree.config = self.config
            return tree.toRPN(top)
        else:
            # attributes, term
            # AttributeElement: attributeType, attributeValue
            # attributeValue ('numeric', n) or ('complex', struct)
            if (self.index.value == 'resultsetid'):
                return ('op', ('resultSet', self.term.value))

            clause = z3950.AttributesPlusTerm()
            attrs = self.index.toRPN(top)
            if (self.term.value.isdigit()):
                self.relation.modifiers.append(CModifierClause('cql.number'))
            relattrs = self.relation.toRPN(top)
            attrs.update(relattrs)
            butes =[]
            for e in attrs.iteritems():
                butes.append((e[0][0], e[0][1], e[1]))

            clause.attributes = [make_attr(*e) for e in butes]
            clause.term = self.term.toRPN(top)

            return ('op', ('attrTerm', clause))


class CBoolean(Boolean):

    def toRPN(self, top):
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

    def toRPN(self, top=None):
        """rpnRpnOp"""
        if not top:
            top = self

        op = z3950.RpnRpnOp()
        op.rpn1 = self.leftOperand.toRPN(top)
        op.rpn2 = self.rightOperand.toRPN(top)
        op.op = self.boolean.toRPN(top)
        return ('rpnRpnOp', op)


class CIndex(Index):
    def toRPN(self, top):
        self.resolvePrefix()
        pf = self.prefix
        if (not pf and self.prefixURI):
            # We have a default
            for k in zConfig.contextSets:
                if zConfig.contextSets[k] == self.prefixURI:
                    pf = k
                    break

        # Default BIB1
        set = oids.oids['Z3950']['ATTRS']['BIB1']['oid']

        if (hasattr(top, 'config') and top.config):
            config = top.config
            # Check SRW Configuration
            cql = config.contextSetNamespaces['cql']
            index = self.value
            if self.prefixURI == cql and self.value == "serverchoice":
            # Have to resolve our prefixes etc, so create an index object to do it
                index = config.defaultIndex
                cidx = CIndex(index)
                cidx.config = config
                cidx.parent = config
                cidx.resolvePrefix()
                pf = cidx.prefix
                index = cidx.value

            if config.indexHash.has_key(pf):
                if config.indexHash[pf].has_key(index):
                    idx = config.indexHash[pf][index]
                    # Need to map from this list to RPN list
                    attrs = {}
                    for i in idx:
                        set = asn1.OidVal(map(int, i[0].split('.')))
                        type = int(i[1])
                        if (i[2].isdigit()):
                            val = int(i[2])
                        else:
                            val = i[2]
                        attrs[(set, type)] = val
                    return attrs
                else:
                    diag = Diagnostic16()
                    diag.details = index
                    diag.message = "Unknown index"
                    raise diag
            else:
                diag = Diagnostic15()
                diag.details = pf
                diag.message = "Unknown context set"
                raise diag
        elif (hasattr(zConfig, pf)):
            mp = getattr(zConfig, pf)
            if (mp.has_key(self.value)):
                val = mp[self.value]
            else:
                val = self.value
        elif (oids.oids['Z3950']['ATTRS'].has_key(pf.upper())):
            set = oids.oids['Z3950']['ATTRS'][pf.upper()]['oid']
            if (self.value.isdigit()):
                # bib1.1018
                val = int(self.value)
            else:
                # complex attribute for bib1
                val = self.value
        else:
            print "Can't resolve %s" % pf
            raise(ValueError)
            
        return {(set, 1) :  val}
            

class CRelation(Relation):
    def toRPN(self, top):
        rels = ['', '<', '<=', '=', '>=', '>', '<>']
        set = z3950.Z3950_ATTRS_BIB1_ov
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
            # vals[6] = 3
        else:
            vals[3] = 3
            # vals[6] = 1

        attrs = {}
        for x in range(1,7):
            if vals[x]:
                attrs[(z3950.Z3950_ATTRS_BIB1_ov, x)] = vals[x]

        return attrs
        

class CTerm(Term):
    def toRPN(self, top):
        return ('general', self.value)

class CModifierClause(ModifierClause):
    pass

class CModifierType(ModifierType):
    pass





