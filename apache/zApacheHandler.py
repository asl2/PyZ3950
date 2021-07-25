
# Use with mod_python (requires post 3.0.3 for improved conn.read())
# Plus CQL and PyZ3950

# In Apache config, for example:
# Listen 127.0.0.1:2100
# <VirtualHost 127.0.0.1:2100>
#      PythonPath "sys.path+['/path/to/code/']"
#      PythonConnectionHandler filenameOfCode
#      PythonDebug On  
# </VirtualHost>

from PyZ3950.asn1 import encode, IncrementalDecodeCtx
from PyZ3950.z3950_2001 import *
from z3950_utils import *
from PyZ3950.zdefs import *
from PyZ3950.oids import *

from mod_python import apache
import traceback
import CQLParser as cql


LOGFILE = "/home/cheshire/log.txt"

def zAttrsToCQL(attrCombinations):
    # XXX Mmmmm. What to do exactly?
    # If we have ZeeRex configs to check, look there.
    # Otherwise we should just do some generic transformations?

    return (str(attrCombinations), "=")


class ZHandler:

    buffer = []
    connection = None
    logfile = None
    handlers = {}
    done = 0
    debug = 1
    ctx = None

    def __init__(self, conn, logf):
        self.connection = conn
        self.logfile = logf
        self.ctx = asn1.IncrementalDecodeCtx(APDU)
        
        self.handlers = {"initRequest" : self.handleInit,
                         "searchRequest" : self.handleSearch,
                         "scanRequest" : self.handleScan,
                         "close" : self.handleClose,
                         "presentRequest" : self.handlePresent,
                         "sortRequest" : self.handleSort,
                         "deleteResultSetRequest" : self.handleDeleteResultSet,
                         "extendedServicesRequest" : self.handleExtendedServices
                         }

    def log(self, text):
        self.logfile.write(text + "\n")
        self.logfile.flush()
        
    def read(self):
        c = self.connection.read()
        while (c):
            try:
                self.ctx.feed(list(map(ord, c)))
                while self.ctx.val_count() > 0:
                    # We have a PDU
                    (type, data) = self.ctx.get_first_decoded()
                    
                    # Successfully decoded.
                    self.log("Received " + type);
                    
                    if (type in self.handlers):
                        resp = self.handlers[type](data)
                        self.connection.write(resp.tostring())
                        self.log("Sent response");
                    else:
                        # Uhoh, unknown request
                        self.log("Ohoh, don't know how to handle " + type)

            except:
                if (self.debug):
                    self.logfile.write("\n")
                    traceback.print_exc(100, self.logfile)
                    self.logfile.flush()
            c = self.connection.read()

    def handleInit(self, req):
        resp = InitializeResponse()
        resp = negotiateCharSet(req, resp)

        resp.protocolVersion = ProtocolVersion()
        resp.protocolVersion['version_1'] = 1
        resp.protocolVersion['version_2'] = 1
        resp.protocolVersion['version_3'] = 1
        
        resp.options = Options()
        for o in ['search', 'present', 'delSet', 'scan', 'negotiation', 'sort']:
            resp.options[o] = 1

        resp.preferredMessageSize = 0x10000
        resp.exceptionalRecordSize = 0x10000
        resp.implementationId = 'Cheshire/PyZ39.50'
        resp.implementationName = 'Cheshire/PyZ39.50 Server'
        resp.implementationVersion = '0.1'
        resp.result = 1
        pdu = asn1.encode(APDU, ('initResponse', resp))
        return pdu

    def handleSearch(self, data):

        queryType = data.query[0]
        query = None
        queryString = ""
        if (queryType in ['type_1', 'type_101']):
            zQuery = data.query[1]
            attrset = zQuery.attributeSet
            rpn = zQuery.rpn

            # Lets try and turn RPN into CQL.
            if rpn[0] == 'op':
                # single search clause
                op = rpn[1]
                query = self.build_searchClause(op, data)
            elif rpn[0] == 'rpnRpnOp':
                triple = rpn[1]
                query = self.build_triple(triple, data)
        elif (queryType == 'type_0'):
            # A Priori external
            queryString = data.query[1]
        elif (queryType == 'type_2'):
            # ISO8777  (CCL)
            queryString = data.query[1]
        elif (queryType == 'type_104'):
            # Look for CQL or SQL
            type104 = data.query[1].direct_reference
            queryString = data.query[1].encoding[1]

            if (type104 == Z3950_QUERY_CQL_ov):
                # Native CQL query
                query = cql.parse(queryString)
            elif (type104 == Z3950_QUERY_SQL_ov):
                # Hopefully just pass off to Postgres
                pass
            else:
                # Undefined query type
                raise NotImplementedError

        elif (queryType in ['type_102', 'type_100']):
            # 102: Ranked List, not yet /defined/ let alone implemented
            # 100: Z39.58 query (Standard was withdrawn)
            raise NotImplementedError

        if query:
            self.log(query.toXCQL())
        elif queryString:
            self.log("type:  " + queryType)
            self.log("query: " + queryString)

        rsetname = data.resultSetName
        dbs = data.databaseNames

        resp = SearchResponse()
        resp.resultCount = 1
        resp.numberOfRecordsReturned = 0
        resp.nextResultSetPosition = 1
        resp.searchStatus = 1
        resp.resultSetStatus = 0
        resp.presentStatus = 0
        # resp.records = ('responseRecords', [])
        pdu = asn1.encode(APDU, ('searchResponse', resp))
        return pdu

    def handleScan(self, data):

        resp = ScanResponse()
        resp.stepSize = 1
        resp.scanStatus = 1
        resp.numberOfEntriesReturned = 0
        resp.positionOfTerm = 0
        resp.entries = ('entries', [])
        pdu = asn1.encode(APDU, ('scanResponse', resp))
        return pdu

    def handlePresent(self, data):
        resp = PresentResponse()
        resp.numberOfRecordsReturned = 1
        resp.nextResultSetPosition = 2
        resp.presentStatus = 1
        resp.records = ('responseRecords', [])
        pdu = asn1.encode(APDU, ('presentResponse', resp))
        return pdu

    def handleClose(self, data):
        resp = Close()
        resp.closeReason = 0
        resp.diagnosticInformation = "Normal Close"
        pdu = asn1.encode(APDU, ('close', resp))
        return pdu

    def handleSort(self, data):
        resp = SortResponse()
        resp.sortStatus = 1
        resp.resultSetStatus = 1
        resp.resultCount = 1
        pdu = asn1.encode(APDU, ('sortResponse', resp))
        return pdu

    def handleDeleteResultSet(self, data):
        resp = DeleteResultSetResponse()
        resp.deleteOperationStatus = 0
        resp.numberNotDeleted = 0
        resp.deleteMessage = "No Resultset"
        pdu = asn1.encode(APDU, ('deleteResultSetResponse', resp))
        return pdu


    def handleExtendedServices(self, data):

        esoids = oids['Z3950']['ES']
        tsp = data.taskSpecificParameters
        package = data.packageType
        self.log("Package")
        self.log(str(package))
        self.log("tSP")
        self.log(str(tsp))
        self.log("persistrs")
        self.log(str(esoids['PERSISTRS']['oid']))
        
        if (package == esoids['PERSISTRS']['oid']):
            pass

        resp = ExtendedServicesResponse()
        resp.operationStatus = 0
        pdu = asn1.encode(APDU, ('extendedServicesResponse', resp))
        return pdu


    def build_searchClause(self, op, data):
        type = op[0]
        
        if type == 'attrTerm':
            attrs = op[1].attributes
            term = op[1].term
            combs = []
            for acomb in attrs:
                if (hasattr(acomb, 'attributeSet')):
                    aset = acomb.attributeSet
                elif(hasattr(data, 'attributeSet')):
                    aset = data.attributeSet
                else:
                    # Oh Man... just assume BIB1
                    aset = Z3950_ATTRS_BIB1_ov

                if (hasattr(acomb, 'attributeType')):
                    atype = acomb.attributeType
                else:
                    # URGH!?
                    atype = 1

                astruct = acomb.attributeValue
                if astruct[0] == 'numeric':
                    avalue = astruct[1]
                else:
                    # complex
                    astruct = astruct[1]
                    if (hasattr(astruct, 'list')):
                        avalue = astruct.list[0][1]
                    else:
                        #semanticAction
                        # Uhh... sequence of int ??
                        avalue = astruct.semanticAction[0][1]
                combs.append([aset, atype, avalue])

            # Need to do real mapping
            sc = cql.SearchClause()
            (index, relation) = zAttrsToCQL(combs)
            sc.index = index
            sc.relation = cql.Relation(relation)
            # XXX term is tuple ('general', 'term')
            # What other than general can we be?
            sc.term = term[1]
            return sc

        else:
            self.log("Not attrTerm: " + repr(op))
            return None


    def build_triple(self, triple):
        bool = triple.op
        lhs = triple.rpn1
        rhs = triple.rpn2

        triple = cql.Triple()

        if (lhs[0] == 'op'):
            lhs = self.build_searchClause(lhs[1])
        else:
            lhs = self.build_triple(lhs[1])
        triple.leftOperand = lhs

        if (rhs[0] == 'op'):
            rhs = self.build_searchClause(rhs[1])
        else:
            rhs = self.build_triple(rhs[1])
        triple.rightOperand = rhs

        triple.boolean = cql.Boolean(bool[0])
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

            mods = [relation, str(distance), unit, order]
            triple.boolean.modifiers = mods
            
        return triple
                              

def connectionhandler(conn):
    # Apache level stuff
    if (conn.local_addr[1] != 2100):
        return apache.DECLINED
    try:
        logfile = file(LOGFILE, "w")
        handler = ZHandler(conn, logfile)
        handler.read()

    except Exception as err:
        logfile.write("Major Failure:\n")
        traceback.print_exc(100, logfile)
        logfile.flush()

    return apache.OK
