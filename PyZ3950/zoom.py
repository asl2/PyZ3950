#!/usr/bin/env python

"""Implements the ZOOM 1.4 API (http://zoom.z3950.org/api)
for Z39.50.

Some global notes on the binding (these will only make sense when read
after the API document):

Get/Set Option is implemented as member attribute access or
assignment.  Implementations are encouraged to throw an AttributeError
for unsupported (or, possibly, mistyped) attributes.  (Production
applications are encouraged to catch such errors.)

All errors are reported as exceptions deriving from ZoomError (or, at
least, it's a bug if they aren't).  Bib1Err is defined as part of the
binding; all the rest are specific to this implementation.

ResultSet provides a sequence interface, with standard Python
iteration, indexing, and slicing.  So if rs is a ResultSet, use len
(rs) for Get_Size and rs[i] for Get_Record, or iterate with for r in
rs: foo(r).  Any attempt to access a record for which the server
returned a surrogate diagnostic will raise the appropriate Bib1Err
exception.

For Record, Render_Record is implemented as Python __str__.  The
'syntax' member contains the string-format record syntax, and the
'data' member contains the raw data.

The following query types are supported:
- "CCL", ISO 8777, (http://www.indexdata.dk/yaz/doc/tools.tkl#CCL)
- "S-CCL", the same, but interpreted on the server side
- "CQL", the Common Query Language, (http://www.loc.gov/z3950/agency/zing/cql/)
- "S-CQL", the same, but interpreted on the server side
- "PQF", Index Data's Prefix Query Format, (http://www.indexdata.dk/yaz/doc/tools.tkl#PQF)
- "C2", Cheshire II query syntax, (http://cheshire.berkeley.edu/cheshire2.html#zfind)
- "ZSQL", Z-SQL, see (http://archive.dstc.edu.au/DDU/projects/Z3950/Z+SQL/)
- "CQL-TREE", a general-purpose escape allowing any object with a toRPN method to be used, e.g. the CQL tree objects

ScanSet, like ResultSet, has a sequence interface.  The i-th element
is a dictionary.  See the ScanSet documentation for supported keys.

Sample usage:
    from PyZ3950 import zoom
    conn = zoom.Connection ('z3950.loc.gov', 7090)
    conn.databaseName = 'VOYAGER'
    conn.preferredRecordSyntax = 'USMARC'
    query = zoom.Query ('CCL', 'ti="1066 and all that"')
    res = conn.search (query)
    for r in res:
            print str(r)
    conn.close ()
I hope everything else is clear from the docstrings and the abstract
API: let me know if that's wrong, and I'll try to do better.

For some purposes (I think the only one is writing Z39.50 servers),
you may want to use the functions in the z3950 module instead.  """

from __future__ import nested_scopes    

__author__ = 'Aaron Lav (asl2@pobox.com)'
__version__ = '1.0' # XXX

import getopt
import sys 

# TODO:
# finish lang/charset (requires charset normalization, confer w/ Adam)
# implement piggyback   
# implement schema    (Non useful)
# implement setname   (Impossible?)

from PyZ3950 import z3950
from PyZ3950 import ccl
from PyZ3950 import asn1
from PyZ3950 import zmarc
from PyZ3950 import bib1msg
from PyZ3950 import grs1
from PyZ3950 import oids

# Azaroth 2003-12-04:
from PyZ3950 import CQLParser, SRWDiagnostics, pqf
from PyZ3950 import c2query as c2
asn1.register_oid (oids.Z3950_QUERY_SQL, z3950.SQLQuery)


def my_enumerate (l): # replace w/ enumerate when we go to Python 2.3
    return zip (range (len (l)), l)

trace_extract = 0
"""trace extracting records from search/present reqs"""

class ZoomError (Exception):
    """Base class for all errors reported from this module"""
    pass

class ConnectionError(ZoomError):
    """Exception for TCP error"""
    pass

class ClientNotImplError (ZoomError):
    """Exception for ZOOM client-side functionality not implemented (bug
       author)"""
    pass

class ServerNotImplError (ZoomError):
    """Exception for function not implemented on server"""
    pass

class QuerySyntaxError (ZoomError):
    """Exception for query not parsable by client"""
    pass

class ProtocolError (ZoomError):
    """Exception for malformatted server response"""
    pass

class UnexpectedCloseError (ProtocolError):
    """Exception for unexpected (z3950, not tcp) close from server"""
    pass

class UnknownRecSyn (ZoomError):
    """Exception for unknown record syntax returned from server"""
    pass

class Bib1Err (ZoomError):
    """Exception for BIB-1 error"""
    def __init__ (self, condition, message, addtlInfo):
        self.condition = condition
        self.message = message
        self.addtlInfo = addtlInfo
        ZoomError.__init__ (self)
    def __str__ (self):
        return "Bib1Err: %d %s %s" % (self.condition, self.message, self.addtlInfo)


class _ErrHdlr:
    """Error-handling services"""
    err_attrslist = ['errCode','errMsg', 'addtlInfo']
    def err (self, condition, addtlInfo, oid):
        """Translate condition + oid to message, save, and raise exception"""
        self.errCode = condition
        self.errMsg  = bib1msg.lookup_errmsg (condition, oid)
        self.addtlInfo = addtlInfo
        raise Bib1Err (self.errCode, self.errMsg, self.addtlInfo)
    def err_diagrec (self, diagrec):
        (typ, data) = diagrec
        if typ == 'externallyDefined':
            raise ClientNotImplErr ("Unknown external diagnostic" + str (data))
        addinfo = data.addinfo [1] # don't care about v2 vs v3
        self.err (data.condition, addinfo, data.diagnosticSetId)
    

_record_type_dict = {}
"""Map oid to renderer, field-counter, and field-getter functions"""

def _oid_to_key (oid):
    for (k,v) in _record_type_dict.items ():
        if v.oid == oid:
            return k
    raise UnknownRecSyn (oid)

def _extract_attrs (obj, attrlist):
    kw = {}
    for key in attrlist:
        if hasattr (obj, key):
            kw[key] = getattr (obj, key)
    return kw

class _AttrCheck:
    """Prevent typos"""
    attrlist = []
    not_implement_attrs = []
    def __setattr__ (self, attr, val):
        """Ensure attr is in attrlist (list of allowed attributes), or
        private (begins w/ '_'), or begins with 'X-' (reserved for users)"""
        if attr[0] == '_' or attr in self.attrlist or attr[0:2] == 'X-':
            self.__dict__[attr] = val
        elif (attr in self.not_implement_attrs):
            raise ClientNotImplError(attr)
        else:
            raise AttributeError (attr, val)
    
class Connection(_AttrCheck, _ErrHdlr):
    """Connection object"""

    not_implement_attrs = ['piggyback',
                        'schema',
                        'proxy',
                        'async']
    search_attrs = ['smallSetUpperBound',
                'largeSetLowerBound',
                'mediumSetPresentNumber',
                'smallSetElementSetNames',
                'mediumSetElementSetNames']
    init_attrs = ['user',
                  'password',
                  'group',
                  'maximumRecordSize',
                  'preferredMessageSize',
                  'lang',
                  'charset',
                  'implementationId',
                  'implementationName',
                  'implementationVersion'
                  ]
    scan_zoom_to_z3950 = {
        # translate names from ZOOM spec to Z39.50 spec names
        'stepSize' : 'stepSize',
        'numberOfEntries' : 'numberOfTermsRequested',
        'responsePosition' : 'preferredPositionInResponse'
        }

    attrlist = search_attrs + init_attrs + scan_zoom_to_z3950.keys () + [
        'databaseName',
        'namedResultSets',
        'preferredRecordSyntax', # these three inheritable by RecordSet
        'elementSetName',
        'presentChunk',
        'targetImplementationId',
        'targetImplementationName',
        'targetImplementationVersion',
        'host',
        'port',

        ] + _ErrHdlr.err_attrslist

    _queryTypes = ['S-CQL', 'S-CCL', 'RPN', 'ZSQL']
    _cli = None
    host = ""
    port = 0

    # and now, some defaults
    namedResultSets = 1
    elementSetName = 'F' 
    preferredRecordSyntax = 'USMARC'
    preferredMessageSize = 0x100000
    maximumRecordSize = 0x100000
    stepSize = 0
    numberOfEntries = 20 # for SCAN
    responsePosition = 1
    databaseName = 'Default'
    implementationId = 'PyZ3950'
    implementationName = 'PyZ3950 1.0/ZOOM v1.4'
    implementationVersion = '1.0'
    lang = None
    charset = None
    user = None
    password = None
    group = None
    presentChunk = 20 # for result sets

    def __init__(self, host, port, connect=1, **kw):
        """Establish connection to hostname:port.  kw contains initial
        values for options, and is useful for options which affect
        the InitializeRequest.  Currently supported values:
        
        user                   Username for authentication
        password               Password for authentication
        group                  Group for authentication
        maximumRecordSize      Maximum size in bytes of one record
        preferredMessageSize   Maximum size in bytes for response
        lang                   3 letter language code
        charset                Character set
        implementationId       Id for client implementation
        implementationName     Name for client implementation
        implementationVersion  Version of client implementation
        
        """

        self.host = host
        self.port = port
        self._resultSetCtr = 0
        for (k,v) in kw.items ():
            setattr (self, k, v)
        if (connect):
            self.connect()

    def connect(self):
        self._resultSetCtr += 1
        self._lastConnectCtr = self._resultSetCtr
        
        # Bump counters first, since even if we didn't reconnect
        # this time, we could have, and so any use of old connections
        # is an error.  (Old cached-and-accessed data is OK to use:
        # cached but not-yet-accessed data is probably an error, but
        # a not-yet-caught error.)
        
        if self._cli <> None and self._cli.sock <> None:
            return
        
        initkw = {}
        for attr in self.init_attrs:
            initkw[attr] = getattr(self, attr)
        if (self.namedResultSets):
            options = ['namedResultSets']
        else:
            options = []
        initkw ['ConnectionError'] = ConnectionError
        initkw ['ProtocolError'] = ProtocolError
        initkw ['UnexpectedCloseError'] = UnexpectedCloseError
        self._cli = z3950.Client (self.host, self.port,
                                  optionslist = options, **initkw)
        self.namedResultSets = self._cli.get_option ('namedResultSets')
        self.targetImplementationId = getattr (self._cli.initresp, 'implementationId', None)
        self.targetImplementationName = getattr (self._cli.initresp, 'implementationName', None)
        self.targetImplementationVersion  = getattr (self._cli.initresp, 'implementationVersion', None)
        if (hasattr (self._cli.initresp, 'userInformationField')):
            # weird.  U of Chicago returns an EXTERNAL with nothing
            # but 'encoding', ('octet-aligned', '2545') filled in.
            if (hasattr (self._cli.initresp.userInformationField,
                         'direct_reference') and
                self._cli.initresp.userInformationField.direct_reference ==
                oids.Z3950_USR_PRIVATE_OCLC_INFO_ov):
# see http://www.oclc.org/support/documentation/firstsearch/z3950/fs_z39_config_guide/ for docs                
                oclc_info = self._cli.initresp.userInformationField.encoding [1]
                # the docs are a little unclear, but I presume we're
                # supposed to report failure whenever a failReason is given.
                
                if hasattr (oclc_info, 'failReason'):
                    raise UnexpectedCloseError ('OCLC_Info ',
                                                oclc_info.failReason,
                                                getattr (oclc_info, 'text',
                                                         ' no text given '))
            
        

    def search (self, query):
        """Search, taking Query object, returning ResultSet"""
        if (not self._cli):
            self.connect()
        assert (query.typ in self._queryTypes)
        dbnames = self.databaseName.split ('+')
        self._cli.set_dbnames (dbnames)
        cur_rsn = self._make_rsn ()
        recv = self._cli.search_2 (query.query,
                                   rsn = cur_rsn,
                                   **_extract_attrs (self, self.search_attrs))
        self._resultSetCtr += 1
        rs = ResultSet (self, recv, cur_rsn, self._resultSetCtr)
        return rs        
    # and 'Error Code', 'Error Message', and 'Addt'l Info' methods still
    # eeded
    def scan (self, query):
        if (not self._cli):
            self.connect()
        self._cli.set_dbnames ([self.databaseName])
        kw = {}
        for k, xl in self.scan_zoom_to_z3950.items ():
            if hasattr (self, k):
                kw [xl] = getattr (self, k)
        return ScanSet (self._cli.scan (query.query, **kw))
    def _make_rsn (self):
        """Return result set name"""
        if self.namedResultSets:
            return "rs%d" % self._resultSetCtr
        else:
            return z3950.default_resultSetName
    def close (self):
        """Close connection"""
        self._cli.close ()
        
    def sort (self, sets, keys):
        """ Sort sets by keys, return resultset interface """
        if (not self._cli):
            self.connect()

        # XXX This should probably be shuffled down into z3950.py
        sortrelations = ['ascending', 'descending', 'ascendingByFrequency', 'descendingByFrequency']

        req = z3950.SortRequest()
        req.inputResultSetNames = []
        for s in sets:
            s._check_stale ()
            req.inputResultSetNames.append(s._resultSetName)
        cur_rsn = self._make_rsn()
        req.sortedResultSetName = cur_rsn

        zkeys = []
        for k in keys:
            zk = z3950.SortKeySpec()
            zk.sortRelation = sortrelations.index(k.relation)
            zk.caseSensitivity = k.caseInsensitive
            if (k.missingValueAction):
                zk.missingValueAction = (k.missingValueAction, None)
            if (k.missingValueData):
                zk.missingValueAction = ('missingValueData', k.missingValueData)
            value = k.sequence
            if (k.type == 'accessPoint'):
                if (value.typ <> 'RPN'):
                    raise ValueError # XXX
                l = z3950.SortKey['sortAttributes']()
                l.id = value.query[1].attributeSet
                l.list = value.query[1].rpn[1][1].attributes
                seq = ('sortAttributes', l)
            elif (k.type == 'private'):
                seq = ('privateSortKey', value)
            elif (k.type == 'elementSetName'):
                spec = z3950.Specification()
                spec.elementSpec = ('elementSetName', value)
                seq = ('elementSpec', spec)
            else:
                raise ValueError # XXX
            spec = ('generic', seq)
            zk.sortElement = spec
            zkeys.append(zk)
        req.sortSequence = zkeys
        recv = self._cli.transact(('sortRequest', req), 'sortResponse')

        self._resultSetCtr += 1
        if (hasattr(recv, 'diagnostics')):
            diag = recv.diagnostics[0][1]
            self.err(diag.condition, diag.addinfo, diag.diagnosticSetId)            

        if (not hasattr(recv, 'resultCount')):
            # First guess: sum of all input sets
            recv.resultCount = 0
            for set in sets:
                recv.resultCount += len(set)
            # Check for addInfo to override
            try:
                val = recv.otherInfo[0].information[1]
                if (val[:14] == 'Result-count: '):
                    recv.resultCount = int(val[14:])
            except:
                pass

        rs = ResultSet (self, recv, cur_rsn, self._resultSetCtr)
        return rs


class SortKey(_AttrCheck):
    attrlist = ['relation', 'caseInsensitive', 'missingValueAction', 'missingValueData', 'type', 'sequence']
    relation = "ascending"
    caseInsensitive = 1
    missingValueAction = ""
    missingValueData = ""
    type = "accessPoint"
    sequence = ""

    def __init__ (self, **kw):
        for k in kw.keys():
            setattr(self, k, kw[k])

class Query:
    def __init__ (self, typ, query):
        """Creates Query object.
Supported query types:  CCL, S-CCL, CQL, S-CQL, PQF, C2, ZSQL, CQL-TREE
"""
        typ = typ.upper()
# XXX maybe replace if ... elif ...  with dict mapping querytype to func
        if typ == 'CCL':
           self.typ = 'RPN'
           try:
               self.query = ccl.mk_rpn_query (query)
           except ccl.QuerySyntaxError, err:
               print "zoom raising", str (err), " for", query
               raise QuerySyntaxError (str(err))
        elif typ == 'S-CCL': # server-side ccl
            self.typ = typ
            self.query =  ('type-2', query)
        elif typ == 'S-CQL': # server-side cql
            self.typ = typ
            xq = asn1.EXTERNAL()
            xq.direct_reference = oids.Z3950_QUERY_CQL_ov
            xq.encoding = ('single-ASN1-type', query)
            self.query = ('type_104', xq)
        elif typ == 'CQL': # CQL to RPN transformation
            self.typ = 'RPN'
            try:
                q = CQLParser.parse(query)
                rpnq = z3950.RPNQuery()
                # XXX Allow Attribute Architecture somehow?
                rpnq.attributeSet = oids.Z3950_ATTRS_BIB1_ov
                rpnq.rpn = q.toRPN()
                self.query = ('type_1', rpnq)
            except SRWDiagnostics.SRWDiagnostic, err:
                raise err
            except:
                raise QuerySyntaxError
        elif typ == 'PQF':  # PQF to RPN transformation
            self.typ = 'RPN'
            try:
                self.query = pqf.parse(query)
            except:
                raise QuerySyntaxError

        elif typ == 'C2': # Cheshire2 Syntax
            self.typ = 'RPN'
            try:
                q = c2.parse(query)
                self.query = q[0]
            except:
                raise QuerySyntaxError
        elif typ == 'ZSQL': # External SQL
            self.typ = typ
            xq = asn1.EXTERNAL()
            xq.direct_reference = oids.Z3950_QUERY_SQL_ov
            q = z3950.SQLQuery()
            q.queryExpression = query
            xq.encoding = ('single-ASN1-type', q)
            self.query = ('type_104', xq)
        elif typ == 'CQL-TREE': # Tree to RPN
            self.typ = 'RPN'
            try:
                rpnq = z3950.RPNQuery()
                # XXX Allow Attribute Architecture
                rpnq.attributeSet = oids.Z3950_ATTRS_BIB1_ov
                rpnq.rpn = query.toRPN()
                self.query = ('type_1', rpnq)
            except SRWDiagnostics.SRWDiagnostic, err:
                raise err
            except:
                raise QuerySyntaxError
        else:
            raise ClientNotImplError ('%s queries not supported' % typ)


class ResultSet(_AttrCheck, _ErrHdlr):
    """Cache results, presenting read-only sequence interface.  If
    a surrogate diagnostic is returned for the i-th record, an
    appropriate exception will be raised on access to the i-th
    element (either access by itself or as part of a slice)."""

    inherited_elts = ['elementSetName', 'preferredRecordSyntax',
                      'presentChunk']
    attrlist = inherited_elts + _ErrHdlr.err_attrslist
    not_implement_attrs = ['piggyback',
                        'schema']

    def __init__ (self, conn, searchResult, resultSetName, ctr):
        """Only for creation by Connection object"""
        self._conn = conn # needed for 'option inheritance', see ZOOM spec
        self._searchResult = searchResult
        self._resultSetName = resultSetName
        self._records = {}
        self._ctr = ctr
        # _records is a dict indexed by preferredRecordSyntax of
        # dicts indexed by elementSetName of lists of records
        self._ensure_recs ()
        
        # whether there are any records or not, there may be
        # nonsurrogate diagnostics.  _extract_recs will get them.
        if hasattr (self._searchResult, 'records'):
            self._extract_recs (self._searchResult.records, 0)
    def __getattr__ (self, key):
        """Forward attribute access to Connection if appropriate"""
        if self.__dict__.has_key (key):
            return self.__dict__[key]
        if key in self.inherited_elts:
            return getattr (self._conn, key) # may raise AttributeError
        raise AttributeError (key)
    def _make_keywords (self):
        """Set up dict of parms for present request"""
        kw = {}
        # need for translation here from preferredRecordSyntax to recsyn
        # is kinda pointless
        if hasattr (self, 'preferredRecordSyntax'):
            try:
                kw['recsyn'] = _record_type_dict [
                    self.preferredRecordSyntax].oid
            except KeyError, err:
                raise ClientNotImplError ('Unknown record syntax ' +
                                          self.preferredRecordSyntax)
        if hasattr (self, 'elementSetName'):
            kw['esn'] = ('genericElementSetName', self.elementSetName)
        return kw
    def __len__ (self):
        """Get number of records"""
        return self._searchResult.resultCount
    def _pin (self, i):
        """Handle negative indices"""
        if i < 0:
            return i + len (self)
        return i
    def _ensure_recs (self):
        if not self._records.has_key (self.preferredRecordSyntax):
            self._records [self.preferredRecordSyntax] = {}
            self._records [self.preferredRecordSyntax][
                self.elementSetName] = [None] * len (self)
        if not self._records[self.preferredRecordSyntax].has_key (
            self.elementSetName):
            self._records [self.preferredRecordSyntax][
                self.elementSetName] = [None] * len (self)

    def _get_rec (self, i):
        return self._records [self.preferredRecordSyntax][
            self.elementSetName][i]

    def _check_stale (self):
        if self._ctr < self._conn._lastConnectCtr:
            raise ConnectionError ('Stale result set used')
        # XXX is this right?
        if (not self._conn.namedResultSets) and \
           self._ctr <> self._conn._resultSetCtr:
            raise ServerNotImplError ('Multiple Result Sets')
        # XXX or this?
    
    def _ensure_present (self, i):
        self._ensure_recs ()
        if self._get_rec (i) == None:
            self._check_stale ()
            maxreq = self.presentChunk
            if maxreq == 0: # get everything at once
                lbound = i
                count = len (self) - lbound
            else:
                lbound = (i / maxreq) * maxreq
                count = min (maxreq, len (self) - lbound)
            kw = self._make_keywords ()
            if self._get_rec (lbound) == None:
                presentResp = self._conn._cli.present (
                    start = lbound + 1,  # + 1 b/c 1-based
                    count = count,
                    rsn = self._resultSetName,
                    **kw)
                if not hasattr (presentResp, 'records'):
                    raise ProtocolError (str (presentResp))
                self._extract_recs (presentResp.records, lbound)
            # Maybe there was too much data to fit into
            # range (lbound, lbound + count).  If so, try
            # retrieving just one record. XXX could try
            # retrieving more, up to next cache bdary.
            if i <> lbound and self._get_rec (i) == None:
                presentResp  = self._conn._cli.present (
                    start = i + 1,
                    count = 1,
                    rsn = self._resultSetName,
                    **kw)
                self._extract_recs (presentResp.records, i)
        rec = self._records [self.preferredRecordSyntax][
            self.elementSetName][i]
        if rec <> None and rec.is_surrogate_diag ():
            rec.raise_exn ()
    def __getitem__ (self, i):
        """Ensure item is present, and return a Record"""
        i = self._pin (i)
        if i >= len (self):
            raise IndexError
        self._ensure_present (i)
        return self._records [self.preferredRecordSyntax][
            self.elementSetName][i]
    def __getslice__(self, i, j):
        i = self._pin (i)
        j = self._pin (j)
        if j > len (self):
            j = len (self)
        for k in range (i, j):
            self._ensure_present (k)
        if len (self._records) == 0: # XXX is this right?
            return []
        return self._records[self.preferredRecordSyntax][
            self.elementSetName] [i:j]
    def _extract_recs (self, records, lbound):
        (typ, recs) = records
        if trace_extract:
            print "Extracting", len (recs), "starting at", lbound
        if typ == 'nonSurrogateDiagnostic':
            self.err (recs.condition, "", recs.diagnosticSetId)
        elif typ == 'multipleNonSurDiagnostics':
            # see Zoom mailing list discussion of 2002/7/24 to justify
            # ignoring all but first error.
            diagRec = recs [0]
            self.err_diagrec (diagRec)
        if (typ <> 'responseRecords'):
            raise ProtocolError ("Bad records typ " + str (typ) + str (recs))
        for i,r in my_enumerate (recs):
            r = recs [i]
            dbname = getattr (r, 'name', '')
            (typ, data) = r.record
            if (typ == 'surrogateDiagnostic'):
                rec = SurrogateDiagnostic (data)

            elif typ == 'retrievalRecord':
                oid = data.direct_reference
                dat = data.encoding
                (typ, dat) = dat
                if (oid == oids.Z3950_RECSYN_USMARC_ov):
                    if typ <> 'octet-aligned':
                        raise ProtocolError (
                            "Weird record EXTERNAL MARC type: " + typ)
                rec = Record (oid, dat, dbname)
            else:
                raise ProtocolError ("Bad typ %s data %s" %
                                     (str (typ), str(data)))
            self._records[self.preferredRecordSyntax][
                self.elementSetName][lbound + i] = rec
    def delete (self): # XXX or can I handle this w/ a __del__ method?
        """Delete result set"""
        res = self._conn._cli.delete (self._resultSetName)
        if res == None: return # server doesn't support Delete
        # XXX should I throw an exn for delete errors?  Probably.

    # and 'Error Code', 'Error Message', and 'Addt'l Info' methods

    def sort(self, keys):
        return self._conn.sort([self], keys)


class SurrogateDiagnostic(_ErrHdlr):
    """Represent surrogate diagnostic.  Raise appropriate exception
    on access to syntax or data, or when raise_exn method is called.
    Currently, RecordSet relies on the return from is_surrogate_diag (),
    and calls raise_exn based on that."""
    def __init__ (self, diagrec):
        self.diagrec = diagrec
    def is_surrogate_diag (self):
        return 1
    def raise_exn (self):
        self.err_diagrec (self.diagrec)
    def __getattr__ (self, attr):
        if attr == 'data' or attr == 'syntax':
            self.raise_exn ()
        return _ErrHdlr.__getattr (self, attr)

class Record:
    """Represent retrieved record.  'syntax' attribute is a string,
      'data' attribute is the data, which is:
      
      USMARC   -- raw MARC data
      SUTRS    -- a string (possibly in the future unicode)
      XML      -- ditto
      GRS-1    -- a tree (see grs1.py for details)
      EXPLAIN  -- a hard-to-describe format (contact me if you're actually \
using this)
      OPAC     -- ditto
      
      Other representations are not yet defined."""
    def __init__ (self, oid, data, dbname):
        """Only for use by ResultSet"""
        self.syntax = _oid_to_key (oid)
        self._rt = _record_type_dict [self.syntax]
        self.data = self._rt.preproc (data)
        self.databaseName = dbname
    def is_surrogate_diag (self):
        return 0
    def get_fieldcount (self):
        """Get number of fields"""
        return self._rt.fieldcount (self.data)
    def get_field (self,spec):
        """Get field"""
        return self._rt.field (self.data, spec)
    def __str__ (self):
        """Render printably"""
        s = self._rt.renderer (self.data)
        return 'Rec: ' + str (self.syntax) + " " + s

class _RecordType:
    """Map syntax string to OID and per-syntax utility functions"""
    def __init__ (self, name, oid, renderer = lambda v:v,
                  fieldcount = lambda v:1, field = None, preproc = lambda v:v):
        """Register syntax"""
        self.oid = oid
        self.renderer = renderer
        self.fieldcount = fieldcount
        self.field = field
        self.preproc = preproc
        _record_type_dict [name] = self

# XXX do I want an OPAC class?  Probably, and render_OPAC should be
# a member function.


def render_OPAC (opac_data):
    s_list = []
    biblio_oid = opac_data.bibliographicRecord.direct_reference
    if (biblio_oid == z3950.Z3950_RECSYN_USMARC_ov):
        bib_marc = zmarc.MARC (opac_data.bibliographicRecord.encoding [1])
        s_list.append ("Bibliographic %s\n" % (str (bib_marc),) )
    else:
        s_list.append ("Unknown bibliographicRecord OID: " + str(biblio_oid))
    for i, hd in my_enumerate (opac_data.holdingsData):
        typ, data = hd
        s_list.append ('Holdings %d:' % (i,))
        if typ == 'holdingsAndCirc':
            def render (item, level = 1):
                s_list = []
                if isinstance (item, asn1.StructBase):
                    for attr, val in item.__dict__.items ():
                        if attr [0] <> '_':
                            s_list.append ("%s%s: %s" % (
                                "\t" * level, attr, "\n".join(render (val, level + 1))))
                elif (isinstance (item, type ([])) and len (item) > 0
                      and isinstance (item [0], asn1.StructBase)):
                    s_list.append ("") # generate newline
                    for i, v in my_enumerate (item):
                        s_list.append ("\t" * (level + 1) + str (i))
                        s_list += render (v, level + 1)
                else:
                    s_list.append (repr (item))
                return s_list
            s_list.append ("\n".join (render (data)))
        elif typ == 'marcHoldingsRecord':
            hold_oid = data.direct_reference
            if hold_oid == z3950.Z3950_RECSYN_USMARC_ov:
                holdings_marc = zmarc.MARC (data.encoding [1])
                s_list.append ("Holdings %s\n" % (str (holdings_marc),))
            else:
                s_list.append ("Unknown holdings OID: " + str (hold_oid))
        else:
            s_list.append ("Unknown holdings type: " + typ)
            # shouldn't happen unless z39.50 definition is extended
    return "\n".join (s_list)

_RecordType ('USMARC', z3950.Z3950_RECSYN_USMARC_ov,
            renderer = lambda v: str(zmarc.MARC(v)))
_RecordType ('UKMARC', z3950.Z3950_RECSYN_UKMARC_ov,
            renderer = lambda v: str(zmarc.MARC(v)))
_RecordType ('SUTRS', z3950.Z3950_RECSYN_SUTRS_ov)
_RecordType ('XML', z3950.Z3950_RECSYN_MIME_XML_ov)
_RecordType ('SGML', z3950.Z3950_RECSYN_MIME_SGML_ov)
_RecordType ('GRS-1', z3950.Z3950_RECSYN_GRS1_ov,
             renderer = lambda v: str (v),
             preproc = grs1.preproc)
_RecordType ('OPAC', z3950.Z3950_RECSYN_OPAC_ov, renderer = render_OPAC)
_RecordType ('EXPLAIN', z3950.Z3950_RECSYN_EXPLAIN_ov,
             renderer = lambda v: str (v))

class ScanSet (_AttrCheck, _ErrHdlr):
    """Hold result of scan.
    """
    zoom_to_z3950 = { # XXX need to provide more processing for attrs, alt 
            'freq'   : 'globalOccurrences',
            'display':  'displayTerm',
            'attrs'  :  'suggestedAttributes',
            'alt'    :  'alternativeTerm',
            'other'  :  'otherTermInfo'}
    attrlist = _ErrHdlr.err_attrslist

    def __init__ (self, scanresp):
        """For internal use only!"""
        self._scanresp = scanresp
        if hasattr (scanresp.entries, 'nonsurrogateDiagnostics'):
            self.err_diagrec (scanresp.entries.nonsurrogateDiagnostics[0])
        # Note that specification says that both entries and
        # nonsurrogate diags can be present.  This code will always
        # raise the exn, and will need to be changed if both are needed.

    def __len__ (self):
        """Return number of entries"""
        return self._scanresp.numberOfEntriesReturned
    def _get_rec (self, i):
        if (not hasattr(self._scanresp.entries, 'entries')):
            raise IndexError
        t = self._scanresp.entries.entries[i]
        if t[0] == 'termInfo':
            return t[1]
        else:
            # Only way asserts can fail here is if someone changes
            # the Z39.50 ASN.1 definitions.
            assert (t[0] == 'surrogateDiagnostic')
            diagRec = t[1]
            if diagRec [0] == 'externallyDefined':
                raise ClientNotImplError (
                    'Scan unknown surrogate diagnostic type: ' +
                                          str (diagRec))
            assert (diagRec[0] == 'defaultFormat')
            defDiagFmt = diagRec [1]
            self.err (defDiagFmt.condition, defDiagFmt.addinfo,
                      defDiagFmt.diagnosticSetId)
    def get_term (self, i):
        """Return term.  Note that get_{term,field,fields} can throw an
        exception if the i'th term is a surrogate diagnostic."""
        return self._get_rec (i).term
    def get_field (self, field, i):
        """Returns value of field:
        term: term
        freq: integer
        display: string
        attrs: currently z3950 structure, should be string of attributes
        alt: currently z3950 structure, should be [string of attrs, term] 
        other: currently z3950 structure, dunno what the best Python representation would be
        """
        f = self.zoom_to_z3950 [field]
        r = self._get_rec (i)
        return r.__dict__[f]
    def get_fields (self, i):
        """Return a dictionary mapping ZOOM's field names to values
        present in the response.  (Like get_field, but for all fields.)"""
        r = self._get_rec (i)
        d = {}
        for k,v in self.zoom_to_z3950.items ():
            val = getattr (r, v, None)
            if val <> None:
                d[k] = val
        d["term"] = self.get_term (i)
        return d
    def _pin (self, i):
        if i < 0:
            return i + len (self)
        return i
    def __getitem__ (self, i):
        return self.get_fields (self._pin (i))
    def __getslice__ (self, i, j):
        i = self._pin (i)
        j = self._pin (j)
        if j > len (self):
            j = len (self)
        return [self.get_fields (k) for k in range (i,j)]



if __name__ == '__main__':
    optlist, args = getopt.getopt (sys.argv[1:], 'h:q:t:f:a:e:v:')
    host = 'LC'
    query = ''
    qtype = 'CCL'
    fmts = ['USMARC']
    esns = ['F']
    validation = None
    for (opt, val) in optlist:
        if opt == '-h':
            host = val
        elif opt == '-q':
            query = val
        elif opt == '-t':
            qtype = val
        elif opt == '-f':
            fmts = val.split (',')
        elif opt == '-e':
            esns = val.split (',')
        elif opt == '-v':
            validation = val.split (',')
            
    rv = z3950.host_dict.get (host)
    if rv == None:
        (name, port, dbname) = host.split (':')
        port = int (port)
    else:
        (name, port, dbname) = rv
    
    conn = Connection (name, port)
    conn.databaseName = dbname

    conn.preferredRecordSyntax = fmts [0]
    def run_one (q):
        try:
            query = Query (qtype, q)
            res = conn.search (query)
            for esn in esns:
                for syn in fmts:
                    print "Syntax", syn, "Esn", esn
                    res.preferredRecordSyntax = syn
                    if esn <> 'NONE':
                        res.elementSetName = esn
                    try:
                        for r in res:
                            print str(r)
                    except ZoomError, err:
                        print "Zoom exception", err.__class__, err
#           res.delete ()
# Looks as if Oxford will close the connection if a delete is sent,
# despite claiming delete support (verified with yaz client, too).
        except ZoomError, err:
            print "Zoom exception", err.__class__, err

                    

    if query == '':
        while 1:
            q_str = raw_input ('CCL query: ')
            if q_str == '': break
            run_one (q_str)
    else:
        run_one (query)
    conn.close ()
