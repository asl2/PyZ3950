#!/usr/bin/python

# Author:  Rob Sanderson (azaroth@liv.ac.uk)
# Distributed and Usable under the GPL 
# Version: 1.2
# Most Recent Changes: Simple SQL transformation, case Insensitivity, getResultSetName
#
# With thanks to Adam from IndexData and Mike Taylor for their valuable input

from shlex import shlex
from string import split, replace, find, lower, count, join
from xml.sax.saxutils import escape
from xml.dom.minidom import Node, parseString
from SRWDiagnostics import *
from types import ListType
import set

errorOnEmptyTerm = 0
errorOnNonPreamblePrefix = 0
errorOnQuotedIdentifier = 0
fullResultSetNameCheck = 1

serverChoiceRelation = "scr"
relations = ['any', 'all', '=', '>=', '<=', '>', '<', 'exact', '<>', 'scr']
relationModifiers = ['stem', 'relevant', 'fuzzy', 'phonetic']
relationSeparator = "/"

simpleBooleans = ['and', 'or', 'not']
complexBooleans = ['prox']
booleanModifiers = [['prox'], ['<=', '>', '<', '>=', '=', '<>'], list(map(str, list(range(0,50)))), ['word', 'sentence', 'paragraph', 'element'], ['unordered', 'ordered']]
booleanModifierTypes = ['', 'relation', 'distance', 'unit', 'ordering']
booleanSeparator = "/"
booleanModifierDiagnostics = ['', Diagnostic40(), Diagnostic41(), Diagnostic42(), Diagnostic43()]

reservedPrefixes = {"srw" : "http://www.loc.gov/zing/cql/srw-indexes/v1.0/"}

def convertIndex(sc, top):
    "Convert srw indexset.index into Cheshire index name"
    idx = sc.index
    config = top.config

    # Strip indexSet
    f = idx.find(".")
    if f >= 0:
        set = idx[:f]
        idx = idx[f+1:]
    else:
        set = ""

    # Look for set in prefixes
    if set in top.prefixes:
        setURI = top.prefixes[set]
        for v in list(config.indexSetNamespaces.keys()):
            if config.indexSetNamespaces[v] == setURI:
                set = v
                break
    elif not set:
        set = config.defaultIndexSet
    elif set not in config.indexSetNamespaces:
        # Unknown index set
        diag = Diagnostic15()
        diag.details = set
        raise diag

    # We may have reassigned to srw based on prefixes, hence this goes here.
    # eg > foo="http://www.loc.gov/zing/srw/srw-indexes/v1.0/ foo.serverchoice
    if set =="srw" and idx == "serverchoice":
            idx = config.defaultIndex
            set = config.defaultIndexSet

    if set =="srw" and idx == "resultsetname":
        return ":"

    if set in config.indexHash and idx in config.indexHash[set]:
        idx = config.indexHash[set][idx]

    if type(idx) == ListType:

        # Need to mung for Word type and Exact
        if sc.relation.value == "exact":
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


def convertIndexSQL(sc, top):
    return sc.index

# Requires changes for:  <= >= <>, and escaped \" in "
# From shlex.py (std library for 2.2)
class CQLshlex(shlex):
    "shlex with additions for CQL parsing"
    quotes = '"'
    commenters = ""
    nextToken = ""

    def read_token(self):
        "Read a token from the input stream (no pushback or inclusions)"

        while 1:
            if (self.nextToken != ""):
                self.token = self.nextToken
                self.nextToken = ""
                # Bah. SUPER ugly non portable
                if self.token == "/":
                    self.state = ' '
                    break
                
            nextchar = self.instream.read(1)
            if nextchar == '\n':
                self.lineno = self.lineno + 1
            if self.debug >= 3:
                print("shlex: in state", repr(self.state),  "I see character:", repr(nextchar), "self.quotes: ", repr(self.quotes))

            if self.state is None:
                self.token = ''        # past end of file
                break
            elif self.state == ' ':
                if not nextchar:
                    self.state = None  # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print("shlex: I see whitespace in whitespace state")
                    if self.token:
                        break   # emit current token
                    else:
                        continue
                elif nextchar in self.commenters:
                    self.instream.readline()
                    self.lineno = self.lineno + 1
                elif nextchar in self.wordchars:
                    self.token = nextchar
                    self.state = 'a'
                elif nextchar in self.quotes:
                    self.token = nextchar
                    self.state = nextchar
                elif nextchar in ['<', '>']:
                    self.token = nextchar
                    self.state = '<'
                else:
                    self.token = nextchar
                    if self.token:
                        break   # emit current token
                    else:
                        continue
            elif self.state == '<':
                # Only accumulate <=, >= or <>

                if self.token == ">" and nextchar == "=":
                    self.token = self.token + nextchar
                    self.state = ' '
                    break
                elif self.token == "<" and nextchar in ['>', '=']:
                    self.token = self.token + nextchar
                    self.state = ' '
                    break
                elif not nextchar:
                    self.state = None
                    break
                elif nextchar == "/":
                    self.state = "/"
                    self.nextToken = "/"
                    break
                elif nextchar in self.wordchars:
                    self.state='a'
                    self.nextToken = nextchar
                    break
                else:
                    self.state = ' '
                    break
                
            
            elif self.state in self.quotes:
                self.token = self.token + nextchar
                # Allow escaped quotes
                if nextchar == self.state and self.token[-2] != '\\':
                    self.state = ' '
                    break
                elif not nextchar:      # end of file
                    if self.debug >= 2:
                        print("shlex: I see EOF in quotes state")
                    # Override SHLEX's ValueError to throw diagnostic
                    diag = Diagnostic14()
                    diag.details = self.token[:-1]
                    raise diag
            elif self.state == 'a':
                if not nextchar:
                    self.state = None   # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.debug >= 2:
                        print("shlex: I see whitespace in word state")
                    self.state = ' '
                    if self.token:
                        break   # emit current token
                    else:
                        continue
                elif nextchar in self.commenters:
                    self.instream.readline()
                    self.lineno = self.lineno + 1
                elif nextchar in self.wordchars or nextchar in self.quotes:
                    self.token = self.token + nextchar
                elif nextchar in ['>', '<']:
                    self.nextToken = nextchar
                    self.state = '<'
                    break
                else:
                    self.pushback = [nextchar] + self.pushback
                    if self.debug >= 2:
                        print("shlex: I see punctuation in word state")
                    self.state = ' '
                    if self.token:
                        break   # emit current token
                    else:
                        continue
        result = self.token
        self.token = ''
        if self.debug > 1:
            if result:
                print("shlex: raw token=" + repr(result))
            else:
                print("shlex: raw token=EOF")
        return result


# String as File helper class
class shlexStream:
    "string as Stream handler for CQLshlex"
    data = ""
    start = 0
    def __init__(self, string):
        self.data = string
    def read(self, length=0):
        if not length:
            return self.data[self.start:]
        else:
            val = self.data[self.start:self.start + length]
            self.start = self.start + length
            return val

    def readlines(self, length=0):
        return [self.data]


class PrefixableObject:
    "Root object for triple and searchClause"
    prefixes = {}
    def addPrefix(self, name, identifier):
        if (name in self.prefixes or name in reservedPrefixes):
            # Error condition
            diag = Diagnostic45()
            raise diag;
        self.prefixes[name] = identifier



class SearchClause (PrefixableObject):
    "Object to represent a CQL searchClause"
    type = "searchClause"
    index = ""
    relation = None
    term = ""
    def __init__(self, map=[]):
        if map:
            self.index = lower(map[0])
            self.relation = map[1]
            self.term = map[2]

    def toC3SQL(self, db, idxs):
        # Generate a single SQL section
        idxObj = db.indexes[self.index]
        kt = idxObj.keyType[0] + "k"
        rel = self.relation.value
        if kt == "sk":
            term = "'%s'" % (self.term.replace("'", "\\'"))
        else:
            term = self.term
        if not kt in idxs:
            idxs.append(kt)
        if not 'idx_' + self.index in idxs:
            idxs.append('idx_' + self.index)

        return ["%s.keyid = idx_%s.keyid and %s.key %s %s and d.docid = idx_%s.docid" % (kt, self.index, kt, rel, term, self.index), idxs]

    def toC3BDB(self, db):
        # We want to do this in one pass so do everything now
        return db.processSearchClause(self.index, self.relation.value, self.term)


    def toXCQL(self, depth=0):
        "Produce XCQL version of the object"
        space = ""
        for x in range(depth):
            space = space + "  "
        xml = space + "<searchClause>\n"
        if self.prefixes:
            xml = xml + space + "  <prefixes>\n"
            for p in list(self.prefixes.keys()):
                xml = xml + space + "    <prefix>\n"
                xml = xml + space + "      <name>" + escape(p) + "</name>\n"
                xml = xml + space + "      <identifier>" + escape(self.prefixes[p]) + "</identifier>\n"
                xml = xml + space + "    </prefix>\n"
            xml = xml + space + "  </prefixes>\n"

        xml = xml + space + "  <index>" + escape(self.index) + "</index>\n"
        xml = xml + self.relation.toXCQL(depth+1)
        xml = xml + space + "  <term>" + escape(self.term) + "</term>\n"
        xml = xml + space + "</searchClause>\n"
        return xml

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

            tlist = split(self.term)
            newtlist = []
            for t in tlist:
                newtlist.append(self.convertMetachars(t))
            
            # Relevance?
            clause = "("
            if "relevant" in self.relation.modifiers:
                clause = clause + idx + " @ {" + join(newtlist) + "} AND "
                
            for t in newtlist:
                clause = clause + idx + " {" + t + "} AND "
            clause = clause[:-5]
            clause = clause + ")"

        elif relation == "any":
            # Split term into words and OR together.

            tlist = split(self.term)
            newtlist = []
            for t in tlist:
                newtlist.append(self.convertMetachars(t))
            
            # Relevance?
            if "relevant" in self.relation.modifiers:
                clause = idx + " @ {" + join(newtlist) + "}"
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

    def convertMetacharsSQL(self, t):
        "Convert SRW meta characters in to SQL's LIKE  meta characters"
        # First escape % and _  (Errr....??)
        # This needs real work, but is probably custom job anyway.

        t = replace(t, '*', '%')
        t = replace(t, '?', '_')

        t = replace(t, "\\^", "^")
        t = replace(t, "\\?", "?")
        t = replace(t, "\\*", "*")
        return t


    def toSQL(self, top=None):
        """ Convert CQL into SQL """
        if top == None:
            top = self

        idx = convertIndexSQL(self, top)

        if self.relation.modifiers:
            diag = Diagnostic20()
            diag.details = self.relation.modifiers[0]
            raise(diag)

        if lower(self.index) == "srw.serverchoice":
            self.relation.value = top.config.defaultRelation
            
        if lower(self.index) == "srw.resultsetname":
            # No resultsets in SQL (could do it with cutesy temp tables though)
            diag = Diagnostic50()
            diag.details="SQL database doesn't support result sets"
            raise diag
            
        elif self.relation.value == "all":
            # Split term into words and AND together.

            tlist = split(self.term)
            newtlist = []
            for t in tlist:
                newtlist.append(self.convertMetacharsSQL(t))

            clause = "("
            for t in newtlist:
                clause = clause + idx + " LIKE '" + t + "' AND "
            clause = clause[:-5]
            clause = clause + ")"

        elif self.relation.value == "any":
            # Split term into words and OR together.

            tlist = split(self.term)
            newtlist = []
            for t in tlist:
                newtlist.append(self.convertMetacharsSQL(t))
            
            clause = "("
            for t in newtlist:
                clause = clause + idx + " LIKE '" + t + "' OR "
            clause = clause[:-4]
            clause = clause + ")"

        elif self.relation.value == "exact":
            clause = idx + " = '" + self.term + "'"

        elif self.relation.value == "=":
            if self.term.isdigit():
                # Numeric
                clause = idx + " = " + self.term
            else:
                # Adjacency
                clause = idx + " = '" + self.term + "'"

        elif self.relation.value in ['>', '<', '>=', '<=', '<>']:
            if self.term.isdigit():
                term = self.term
            else:
                term = "'" + self.term + "'"

            clause = idx + " " + self.relation.value + " " + term + ""

        return clause

    def getResultSetName(self, top=None):
        if top == None:
            top = self
        config = top.config
        idx = self.index
        # Strip indexSet
        f = idx.find(".")
        if f >= 0:
            set = lower(idx[:f])
            idx = lower(idx[f+1:])
        else:
            set = ""

        # Look for set in prefixes
        if set in top.prefixes:
            setURI = top.prefixes[set]
            # Translate to local short form
            for v in list(config.indexSetNamespaces.keys()):
                if config.indexSetNamespaces[v] == setURI:
                    set = v
                    break
        elif not set:
            set = config.defaultIndexSet
        elif set not in config.indexSetNamespaces:
            # Unknown index set
            diag = Diagnostic15()
            diag.details = set
            raise diag
        
        if set == "srw" and lower(idx) == "resultsetname" and self.relation.value == "=":
            return self.term
        else:
            return ""

class Relation:
    "Object to represent a CQL relation"
    type = "relation"
    value = ""
    modifiers = []
    def __init__(self, rel='', mods=[]):
        self.value = rel
        self.modifiers = mods
    def toXCQL(self, depth=0):
        "Create XCQL representation of object"
        space = ""
        for x in range(depth):
            space = space + "  "
        xml = space + "<relation>\n"
        xml = xml + space + "  <value>" + escape(self.value) + "</value>\n"
        if self.modifiers:
            xml = xml + space + "  <modifiers>\n"
            for m in self.modifiers:
                xml = xml + space + "    <modifier><value>" + escape(m) + "</value></modifier>\n"
            xml = xml + space + "  </modifiers>\n"
        xml = xml + space + "</relation>\n"
        return xml

class Boolean:
    "Object to represent a CQL boolean"
    type = "boolean"
    value = ""
    modifiers = []
    def __init__(self, bool='', mods=[]):
        self.value = bool
        self.modifiers = mods

    def toXCQL(self, depth=0):
        "Create XCQL representation of object"
        space = ""
        for x in range(depth):
            space = space + "  "
        xml = space + "<boolean>\n"
        xml = xml + space + "  <value>" + escape(self.value) + "</value>\n"
        if self.modifiers:
            modified = 0
            for m in range(1, len(self.modifiers)+1):
                if (self.modifiers[m-1] != ''):
                    if not modified:
                        modified = 1
                        xml = xml + space + "  <modifiers>\n"
                    xml = xml + space + "    <modifier><type>%s</type><value>%s</value></modifier>\n" % (booleanModifierTypes[m], escape(self.modifiers[m-1]))
            if modified:
                xml = xml + space + "  </modifiers>\n"
        xml = xml + space + "</boolean>\n"
        return xml

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

    def toSQL(self):
        if self.modifiers:
            # Can't do proximity
            diag = SRWDiagnostic39()
            diag.details = "SQL doesn't support Proximity"
            raise(diag)
        elif self.value == "not":
            return " and not "
        else:
            return " " + self.value + " "

 
class Triple (PrefixableObject):
    "Object to represent a CQL triple"
    type = "triple"
    leftOperand = None
    boolean = None
    rightOperand = None

    def toXCQL(self, depth=0):
        "Create the XCQL representation of the object"
        space = ""
        for x in range(depth):
            space = space + "  "
        xml = space + "<triple>\n"

        if self.prefixes:
            xml = xml + space + "  <prefixes>\n"
            for p in list(self.prefixes.keys()):
                xml = xml + space + "    <prefix>\n"
                xml = xml + space + "      <name>" + escape(p) + "</name>\n"
                xml = xml + space + "      <identifier>" + escape(self.prefixes[p]) + "</identifier>\n"
                xml = xml + space + "    </prefix>\n"
            xml = xml + space + "  </prefixes>\n"

        xml = xml + self.boolean.toXCQL(depth+1)
        xml = xml + space + "  <leftOperand>\n"
        xml = xml + self.leftOperand.toXCQL(depth+2)
        xml = xml + space + "  </leftOperand>\n"
        xml = xml + space + "  <rightOperand>\n"
        xml = xml + self.rightOperand.toXCQL(depth+2)
        xml = xml + space + "  </rightOperand>\n"
        xml = xml + space + "</triple>\n"
        return xml

    def toC3SQL(self, db, idxs):
        (left, idxs) = self.leftOperand.toC3SQL(db, idxs)
        (right, idxs) = self.rightOperand.toC3SQL(db, idxs)
        bool = self.boolean.value
        return ["(%s) %s (%s)" % (left, bool, right), idxs]

    def toC3BDB(self, db):
        l = self.leftOperand.toC3BDB(db)
        r = self.rightOperand.toC3BDB(db)
        bool = self.boolean.value
        ls = set.set(l)
        rs = set.set(r)
        if bool == 'and':
            return list(ls & rs)
        elif bool == 'or':
            return list(ls | rs)
        elif bool == "not":
            return list(ls - rs)
        else:
            raise ValueError
        

    def toCheshire(self, top=None):
        """ Convert triple into Cheshire search clause """
        if top == None:
            top = self
        string = "(" + self.leftOperand.toCheshire(top) + self.boolean.toCheshire() + self.rightOperand.toCheshire(top) + ")"
        return string

    def toSQL(self, top=None):
        """ Convert into SQL """
        if top == None:
            top = self
        string = "(" + self.leftOperand.toSQL(top) + self.boolean.toSQL() + self.rightOperand.toSQL(top) + ")"
        return string

    def getResultSetName(self, top=None):

        if fullResultSetNameCheck == 0 or self.boolean.value in ['not', 'prox']:
            return ""

        if top == None:
            topLevel = 1
            top = self;
        else:
            topLevel = 0

        # Iterate over operands and build a list
        rsList = []
        if self.leftOperand.type == "triple":
            rsList.extend(self.leftOperand.getResultSetName(top))
        else:
            rsList.append(self.leftOperand.getResultSetName(top))
        if self.rightOperand.type == "triple":
            rsList.extend(self.rightOperand.getResultSetName(top))
        else:
            rsList.append(self.rightOperand.getResultSetName(top))            

        if topLevel == 1:
            # Check all elements are the same, if so we're a fubar form of present
            if (len(rsList) == rsList.count(rsList[0])):
                return rsList[0]
            else:
                return ""
        else:
            return rsList


class CQLParser:
    "Token parser to create object structure for CQL"
    parser = ""
    currentToken = ""
    nextToken = ""

    def __init__(self, p):
        """ Initialise with shlex parser """
        self.parser = p
        self.fetch_token() # Fetches to next
        self.fetch_token() # Fetches to curr

    def is_relation(self, token):
        "Is the token a relation"
        return token in relations

    def is_boolean(self, token):
        "Is the token a boolean"
        if (token in simpleBooleans):
            return 1
        elif (token in complexBooleans):
            return 1
        else:
            return 0

    def fetch_token(self):
        """ Read ahead one token """
        tok = self.parser.get_token()
        self.currentToken = self.nextToken
        self.nextToken = tok

    def prefixes(self):
        "Create prefixes dictionary"
        prefs = {}
        while (self.currentToken == ">"):
            # Strip off maps
            self.fetch_token()
            if self.nextToken == "=":
                # Named map
                name = self.currentToken
                self.fetch_token() # = is current
                self.fetch_token() # id is current
                identifier = self.currentToken
                self.fetch_token()
            else:
                name = ""
                identifier = self.currentToken
                self.fetch_token()
            if (name in prefs):
                # Error condition
                diag = Diagnostic45()
                diag.details = name
                raise diag;
            if len(identifier) > 1 and identifier[0] == '"' and identifier[-1] == '"':
                identifier = identifier[1:-1]
            prefs[lower(name)] = identifier

        return prefs


    def query(self):
        """ Parse query """
        prefs = self.prefixes()
        if prefs and errorOnNonPreamblePrefix:
            diag = Diagnostic10();
            diag.details="Prefix not in Preamble: " + str(prefs)
            raise diag

        left = self.subQuery()
        while 1:
            bool = self.is_boolean(lower(self.currentToken))
            if bool:
                boolobject = self.boolean()
                right = self.subQuery()
                # Setup Left Object
                trip = Triple()
                trip.leftOperand = left
                trip.boolean = boolobject
                trip.rightOperand = right
                left = trip
            else:
                break;

        for p in list(prefs.keys()):
            left.addPrefix(p, prefs[p])
        return left

    def subQuery(self):
        """ Find either query or clause """
        if self.currentToken == "(":
            self.fetch_token() # Skip (
            object = self.query()
            if self.currentToken == ")":
                self.fetch_token() # Skip )
            else:
                diag = Diagnostic13()
                diag.details = self.currentToken
                raise diag
        else:
            object = self.clause()
        return object

    def clause(self):
        """ Find searchClause """

        rel = self.is_relation(lower(self.nextToken))
        bool = self.is_boolean(lower(self.nextToken))

        if rel:
            if '"' in self.currentToken:
                if errorOnQuotedIdentifier:
                    diag = Diagnostic14()
                    diag.details = self.currentToken
                    raise diag
                else:
                    self.currentToken = self.currentToken[1:-1]
            
            irt = SearchClause()
            irt.prefixes = {}
            irt.index = lower(self.currentToken)
            self.fetch_token()   # Skip Index
            rel = self.relation()
            irt.relation = rel

            if self.currentToken in ['>=', '<=', '>', '<', '<>', "/", '=']:
                diag = Diagnostic25()
                diag.details = self.currentToken
                raise diag

            irt.term = self.currentToken
            self.fetch_token()   # Skip Term 
        elif self.currentToken and (bool or self.nextToken in [')', '']):

            if self.currentToken in ['>=', '<=', '>', '<', '<>', "/", '=']:
                diag = Diagnostic25()
                diag.details = self.currentToken
                raise diag

            irt = SearchClause(["srw.serverchoice", Relation(serverChoiceRelation), self.currentToken])
            irt.prefixes = {}
            self.fetch_token()

        elif self.currentToken == ">" and errorOnNonPreamblePrefix == 0:
            prefs = self.prefixes()
            # iterate to get object
            object = self.clause()
            for p in list(prefs.keys()):
                object.addPrefix(p, prefs[p]);
            return object
            
        else:
            diag = Diagnostic10()
            diag.details = "Expected Boolean or Relation but got: " + self.currentToken
            raise diag

        # Unescape quotes
        if (irt.term and irt.term[0] == '"' and irt.term[-1] == '"'):
            irt.term = irt.term[1:-1]
            irt.term = replace(irt.term, '\\"', '"') 
        elif not irt.term:
            # Term is not present, not empty
            diag = Diagnostic10()
            diag.details = "Term not present."
            raise diag


        # Check for badly placed \s
        startidx = 0
        idx = find(irt.term, "\\", startidx)
        while (idx > -1):
            startidx = idx+1
            if not irt.term[idx+1] in ['?', '\\', '*', '^']:
                diag = Diagnostic26()
                diag.details = irt.term
                raise diag
            idx = find(irt.term, "\\", startidx)

        nonanchor = 0
        if irt.term:
            for c in irt.term:
                if c != "^":
                    nonanchor = 1
                    break
            if not nonanchor:
                diag = Diagnostic32()
                diag.details = "Only anchoring character(s) in term: "  + self.currentToken
                raise diag
        elif errorOnEmptyTerm:
            diag = Diagnostic27()
            diag.details = self.currentToken
            raise diag
        return irt

    def boolean(self):
        """ Find boolean """
        self.currentToken = lower(self.currentToken)
        if self.currentToken in simpleBooleans:
            bool = Boolean(self.currentToken)
            self.fetch_token()
        elif self.currentToken in complexBooleans:
            # Step over separators
            bool = Boolean(self.currentToken)
            self.fetch_token()
            subtokens = []

            while (self.currentToken == booleanSeparator):
                self.fetch_token() # Skip /
                self.currentToken = lower(self.currentToken)
                if self.currentToken != booleanSeparator:
                    subtokens.append(self.currentToken)
                    self.fetch_token()
                else:
                    subtokens.append('')

            for s in range(4):
                if len(subtokens) > s:
                    sub = subtokens[s]
                    if sub != '' and not sub in booleanModifiers[s+1]:
                        diag = booleanModifierDiagnostics[s+1]
                        diag.details = sub
                        raise diag
                else:
                    subtokens.append('')
            bool.modifiers = subtokens
        else:
            diag = Diagnostic37()
            diag.details = self.currentToken
            raise diag
                
        return bool

    def relation(self):
        """ Find relation """
        self.currentToken = lower(self.currentToken)
        if self.currentToken in relations:
            # Step over separators
            rel = Relation(self.currentToken)
            self.fetch_token()
            subtokens = []
            while (self.currentToken == relationSeparator):
                self.fetch_token()
                self.currentToken = lower(self.currentToken)
                if self.currentToken == relationSeparator:
                    diag = Diagnostic20()
                    diag.details = "Null relation modifier"
                    raise diag
                elif not self.currentToken in relationModifiers:
                    diag = Diagnostic20()
                    diag.details = self.currentToken
                    raise diag
                else:
                    subtokens.append(self.currentToken)
                    self.fetch_token()
            rel.modifiers = subtokens
        else:
            diag = Diagnostic19()
            diag.details = self.currentToken
            raise diag

        return rel



class XCQLParser:
    """ Parser for XCQL using simple DOM """

    def firstChildElement(self, elem):
        """ Find first child which is an Element """
        for c in elem.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:
                return c
        return None

    def firstChildData(self,elem):
        """ Find first child which is Data """
        for c in elem.childNodes:
            if c.nodeType == Node.TEXT_NODE:
                return c
        return None

    def searchClause(self, elem):
        """ Process a <searchClause> """
        sc = SearchClause()
        for c in elem.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:
                if c.localName == "index":
                    sc.index = lower(self.firstChildData(c).data)
                elif c.localName == "term":
                    sc.term = self.firstChildData(c).data
                elif c.localName == "relation":
                    sc.relation = self.relation(c)
                elif c.localName == "prefixes":
                    sc.prefixes = self.prefixes(c)
                else:
                    raise ValueError
        return sc

    def triple(self, elem):
        """ Process a <triple> """
        trip = Triple()
        for c in elem.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:
                if c.localName == "boolean":
                    trip.boolean = self.boolean(c)
                elif c.localName == "prefixes":
                    trip.prefixes = self.prefixes(c)
                elif c.localName == "leftOperand":
                    c2 = self.firstChildElement(c)
                    if c2.localName == "searchClause":
                        trip.leftOperand = self.searchClause(c2)
                    else:
                        trip.leftOperand = self.triple(c2)
                else:
                    c2 = self.firstChildElement(c)
                    if c2.localName == "searchClause":
                        trip.rightOperand = self.searchClause(c2)
                    else:
                        trip.rightOperand = self.triple(c2)
        return trip

    def relation(self, elem):
        """ Process a <relation> """
        rel = Relation()
        for c in elem.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:
                if c.localName == "value":
                    rel.value = lower(c.firstChild.data)
                elif c.localName == "modifiers":
                    mods = []
                    for c2 in c.childNodes:
                        if c2.nodeType == Node.ELEMENT_NODE:
                            if c2.localName == "modifier":
                                for c3 in c2.childNodes:
                                    if c3.localName == "value":
                                        val = lower(self.firstChildData(c2).data)
                                        mods.append(val)
                    rel.modifiers = mods
        return rel

    def boolean(self, elem):
        "Process a <boolean>"
        bool = Boolean()
        for c in elem.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:
                if c.localName == "value":
                    bool.value = lower(self.firstChildData(c).data)
                else:
                    # Can be in any order, so we need to extract, then order
                    mods = {}
                    for c2 in c.childNodes:
                        if c2.nodeType == Node.ELEMENT_NODE:
                            if c2.localName == "modifier":
                                type = ""
                                value = ""
                                for c3 in c2.childNodes:
                                    if c3.nodeType == Node.ELEMENT_NODE:
                                        if c3.localName == "value":
                                            value = lower(self.firstChildData(c3).data)
                                        elif c3.localName == "type":
                                            type = self.firstChildData(c3).data
                                mods[type] = value

                    modlist = []
                    for t in booleanModifierTypes[1:]:
                        if t in mods:
                            modlist.append(mods[t])
                        else:
                            modlist.append('')
                    bool.modifiers = modlist
        return bool
        
    def prefixes(self, elem):
        "Process <prefixes>"
        prefs = {}
        for c in elem.childNodes:
            if c.nodeType == Node.ELEMENT_NODE:
                # prefix
                name = ""
                identifier = ""
                for c2 in c.childNodes:
                    if c2.nodeType == Node.ELEMENT_NODE:
                        if c2.localName == "name":
                            name = lower(self.firstChildData(c2).data)
                        elif c2.localName == "identifier":
                            identifier = self.firstChildData(c2).data
                prefs[name] = identifier
        return prefs


def xmlparse(s):
    """ API. Return a seachClause/triple object from XML string """
    doc = parseString(s)
    q = xcqlparse(doc.firstChild)
    return q

def xcqlparse(query):
    """ API.  Return a searchClause/triple object from XML DOM objects"""
    # Requires only properties of objects so we don't care how they're generated
    # And don't need to include xml.dom.minidom ourselves

    p = XCQLParser()
    if query.localName == "searchClause":
        return p.searchClause(query)
    else:
        return p.triple(query)


def parse(query):
    """ API. Return a searchClause/triple object from CQL string"""

    q = shlexStream(query)
    lexer = CQLshlex(q)
    lexer.wordchars = lexer.wordchars + "!@#$%^&*-+{}[];,.?|~`:\\"
    parser = CQLParser(lexer)
    object = parser.query()
    if parser.currentToken != '':
        diag = Diagnostic10()
        diag.details = "Unprocessed tokens remain: " + parser.currentToken
        raise diag

    return object

if (__name__ == "__main__"):
    import sys;
    s = sys.stdin.readline()
    try:
        q = parse(s);
    except SRWDiagnostic as diag:
        # Print a full version, not just str()
        print("Diagnostic Generated.")
        print("  Code:        " + str(diag.code))
        print("  Details:     " + str(diag.details))
        print("  Description: " + diag.description)
    else:
        print(q.toXCQL()[:-1]);
    
