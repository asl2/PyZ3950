#!/usr/bin/env python

# This file should be available from
# http://www.pobox.com/~asl2/software/PyZ3950/
# and is licensed under the X Consortium license:
# Copyright (c) 2001, Aaron S. Lav, asl2@pobox.com
# All rights reserved. 

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, provided that the above
# copyright notice(s) and this permission notice appear in all copies of
# the Software and that both the above copyright notice(s) and this
# permission notice appear in supporting documentation. 

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL
# INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 

# Except as contained in this notice, the name of a copyright holder
# shall not be used in advertising or otherwise to promote the sale, use
# or other dealings in this Software without prior written authorization
# of the copyright holder. 

# Change history:
# 2002/05/23
# Fix for Python2 compatibility.  Thanks to Douglas Bates <bates@stat.wisc.edu>
# Fix to support SUTRS (requires asn1 updates, too)
# 2002/05/28
# Make SUTRS printing a little more useful
# Correctly close connection when done
# Handle receiving diagnostics instead of records a little better

"""<p>PyZ3950 currently is capable of sending and receiving v2 or v3 PDUs
Initialize, Search, Present, Scan, Sort, Close, and Delete.  For client
work, you probably want to use ZOOM, which should be in the same
distribution as this file, in zoom.py.  The Server class in this file
implements a server, but could use some work.  Both interoperate with
the <a href="http://www.indexdata.dk/yaz"> Yaz toolkit</a> and the
client interoperates with a variety of libraries.  <p>

Useful resources:
<ul>
<li><a href="http://lcweb.loc.gov/z3950/agency/">
Library of Congress Z39.50 Maintenance Agency Page</a></li>
<li><a href="http://lcweb.loc.gov/z3950/agency/document.html">
Official Specification</a></li>
<li><a href="http://www.loc.gov/z3950/agency/clarify/">Clarifications</a></li>
</ul>
"""

from __future__ import nested_scopes
import getopt
import sys
import exceptions
import random
import socket
import string
import traceback

import codecs

from PyZ3950 import asn1
from PyZ3950 import zmarc
from PyZ3950.zdefs import *

out_encoding = None

trace_recv = 0
trace_init = 0

print_hex = 0

class Z3950Error(Exception):
    pass

# Note: following 3 exceptions are defaults, but can be changed by
# calling conn.set_exs

class ConnectionError(Z3950Error): # TCP or other transport error
    pass

class ProtocolError(Z3950Error): # Unexpected message or badly formatted
    pass

class UnexpectedCloseError(ProtocolError):
    pass

vers = '0.62'
default_resultSetName = 'default'


DEFAULT_PORT = 2101

Z3950_VERS = 3 # This is a global switch: do we support V3 at all?

def extract_recs (resp):
    (typ, recs) = resp.records
    if (typ <> 'responseRecords'):
        raise ProtocolError ("Bad records typ " + str (typ) + str (recs))
    if len (recs) == 0:
        raise ProtocolError ("No records")
    fmtoid = None
    extract = []
    for r in recs:
        (typ, data) = r.record
        if (typ <> 'retrievalRecord'):
            raise ProtocolError ("Bad typ %s data %s" % (str (typ), str(data)))
        oid = data.direct_reference
        if fmtoid == None:
            fmtoid = oid
        elif fmtoid <> oid:
            raise ProtocolError (
                "Differing OIDs %s %s" % (str (fmtoid), str (oid)))
        # Not, strictly speaking, an error.
        dat = data.encoding
        (typ, dat) = dat
        if (oid == Z3950_RECSYN_USMARC_ov):
            if typ <> 'octet-aligned':
                raise ProtocolError ("Weird record EXTERNAL MARC type: " + typ)
        extract.append (dat)
    return (fmtoid, extract)

def get_formatter (oid):
    def printer (x):
        print oid, repr (x)
    def print_marc (marc):
        print str (zmarc.MARC(marc))
    def print_sutrs (x):
        print "SUTRS:",
        if isinstance (x, type ('')):
            print x
        elif isinstance (x, type (u'')):
            if out_encoding == None:
                print repr (x)
            else:
                try:
                    print x.encode (out_encoding)
                except UnicodeError, u:
                    print "Cannot print %s in current encoding %s" % (
                        repr (x), out_encoding)
    if oid == Z3950_RECSYN_SUTRS_ov:
        return print_sutrs
    if oid == Z3950_RECSYN_USMARC_ov:
        return print_marc
    else:
        return printer

def disp_resp (resp):
    try:
        (fmtoid, recs) = extract_recs (resp)
    except ProtocolError, val:
        print "Bad records", str (val)
    formatter = get_formatter (fmtoid)
    for rec in recs:
        formatter (rec)

class Conn:
    rdsz = 65536
    def __init__ (self, sock = None, ConnectionError = ConnectionError,
                  ProtocolError = ProtocolError, UnexpectedCloseError =
                  UnexpectedCloseError):
        self.set_exns (ConnectionError, ProtocolError, UnexpectedCloseError)
        if sock == None:
            self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.decode_ctx = asn1.IncrementalDecodeCtx (APDU)
        self.encode_ctx = asn1.Ctx ()
    def set_exns (self, conn, protocol, unexp_close):
        self.ConnectionError = conn
        self.ProtocolError = protocol
        self.UnexpectedCloseError = unexp_close

    def set_codec (self, charset_name, charsets_in_records):
        self.charset_name = charset_name
        self.charsets_in_records = not not charsets_in_records # collapse None and 0
        if trace_charset:
            print "Setting up codec!", self.charset_name
        strip_bom = self.charset_name == 'utf-16'
        # XXX should create a new codec which wraps utf-16 but
        # strips the Byte Order Mark, or use stream codecs
        if self.charset_name <> None:
            self.encode_ctx.set_codec (asn1.GeneralString,
                                       codecs.lookup (self.charset_name),
                                       strip_bom)
            self.decode_ctx.set_codec (asn1.GeneralString,
                                       codecs.lookup (self.charset_name),
                                       strip_bom)
            if not charsets_in_records: # None or 0
                register_retrieval_record_oids(self.decode_ctx)
                register_retrieval_record_oids(self.encode_ctx)
            
    def readproc (self):
        if self.sock == None:
            raise self.ConnectionError ('disconnected')
        try:
            b = self.sock.recv (self.rdsz)
        except socket.error, val:
            self.sock = None
            raise self.ConnectionError ('socket', str (val))
        if len (b) == 0: # graceful close
            self.sock = None
            raise self.ConnectionError ('graceful close')
        if trace_recv:
            print map (lambda x: hex(ord(x)), b)
        return b
    def read_PDU (self):
        while 1:
            if self.decode_ctx.val_count () > 0:
                return self.decode_ctx.get_first_decoded ()
            try:
                b = self.readproc ()
                self.decode_ctx.feed (map (ord, b))
            except asn1.BERError, val:
                raise self.ProtocolError ('ASN1 BER', str(val))


class Server (Conn):
    test = 0
    def __init__ (self, sock):
        Conn.__init__ (self, sock)
        self.expecting_init = 1
        self.done = 0
        self.result_sets = {}
        self.charset_name = None
    def run (self):
        while not self.done:
            (typ, val) = self.read_PDU ()
            fn = self.fn_dict.get (typ, None)
            if fn == None:
                raise self.ProtocolError ("Bad typ", typ + " " + str (val))
            if typ <> 'initRequest' and self.expecting_init:
                raise self.ProtocolError ("Init expected", typ)
            fn (self, val)
    def send (self, val):
        b = self.encode_ctx.encode (APDU, val)
        if self.test:
            print "Internal Testing"
            # a reminder not to leave this switched on by accident
            self.decode_ctx.feed (b)
            decoded = self.read_PDU ()
            assert (val== decoded)
        self.sock.send (b)

    def do_close (self, reason, info):
        close = Close ()
        close.closeReason = reason
        close.diagnosticInformation = info
        self.send (('close', close))

    def close (self, parm):
        self.done = 1
        self.do_close (0, 'Normal close')
        
    def search_child (self, query):
        return range (random.randint (2,10))
    def search (self, sreq):
        if sreq.replaceIndicator == 0 and self.result_sets.has_key (
            sreq.resultSetName):
            raise self.ProtocolError ("replaceIndicator 0")
        result = self.search_child (sreq.query)
        sresp = SearchResponse ()
        self.result_sets[sreq.resultSetName] = result
        sresp.resultCount = len (result)
        sresp.numberOfRecordsReturned = 0
        sresp.nextResultSetPosition = 1
        sresp.searchStatus = 1
        sresp.resultSetStatus = 0
        sresp.presentStatus = PresentStatus.get_num_from_name ('success')
        sresp.records = ('responseRecords', [])
        self.send (('searchResponse', sresp))
    def format_records (self, start, count, res_set, prefsyn):
        l = []
        for i in range (start - 1, start + count - 1):
            elt = res_set[i]
            elt_external = asn1.EXTERNAL ()
            elt_external.direct_reference = Z3950_RECSYN_SUTRS_ov

            # Not only has this text been extensively translated, but
            # it also prefigures Z39.50's separation of Search and Present,
            # once rearranged a little.
            strings = [
                'seek, and ye shall find; ask, and it shall be given you',
                u"""Car quiconque demande re\u00e7oit, qui cherche trouve, et \u00e0 quit frappe on ouvrira""", # This (next) verse has non-ASCII characters
                u"\u0391\u03b9\u03c4\u03b5\u03b9\u03c4\u03b5, "
                u"\u03ba\u03b1\u03b9 \u03b4\u03bf\u03b8\u03b7\u03c3\u03b5\u03c4\u03b1\u03b9 "+ 
                u"\u03c5\u03bc\u03b9\u03bd; \u03b6\u03b7\u03c4\u03b5\u03b9\u03c4\u03b5 " + 
                u"\u03ba\u03b1\u03b9 \u03b5\u03c5\u03c1\u03b7\u03c3\u03b5\u03c4\u03b5",
                u"\u05e8\u05d0\u05d4 \u05d6\u05d4 \u05de\u05e6\u05d0\u05ea\u05d9"]
            if self.charsets_in_records:
                encode_charset = self.charset_name
            else:
                encode_charset = 'ascii'
            def can_encode (s):
                try:
                    s.encode (encode_charset)
                except UnicodeError:
                    return 0
                return 1
            if self.charset_name == None:
                candidate_strings = [strings[0]]
            else:
                candidate_strings = [s for s in strings if can_encode (s)]
            # Note: this code is for debugging/testing purposes.  Usually,
            # language/content selection should not be made on the
            # basis of the selected charset, and a surrogate diagnostic
            # should be generated if the data cannot be encoded.
            text = random.choice (candidate_strings) 
            add_str = " #%d charset %s cir %d" % (elt, encode_charset,
                                              self.charsets_in_records)
            elt_external.encoding = ('single-ASN1-type', text + add_str)
            n = NamePlusRecord ()
            n.name = 'foo'
            n.record = ('retrievalRecord', elt_external)
            l.append (n)
        return l
        
    def present (self, preq):
        presp = PresentResponse ()
        res_set = self.result_sets [preq.resultSetId]
        presp.numberOfRecordsReturned = preq.numberOfRecordsRequested
        presp.nextResultSetPosition = preq.resultSetStartPoint + \
                                      preq.numberOfRecordsRequested
        presp.presentStatus = 0
        presp.records = ('responseRecords',
                         self.format_records (preq.resultSetStartPoint,
                                              preq.numberOfRecordsRequested,
                                              res_set,
                                              preq.preferredRecordSyntax))
        self.send (('presentResponse', presp))
        
    def init (self, ireq):
        if trace_init:
            print "Init received", ireq
        self.v3_flag = (ireq.protocolVersion ['version_3'] and
                        Z3950_VERS == 3)
        
        ir = InitializeResponse ()
        ir.protocolVersion = ProtocolVersion ()
        ir.protocolVersion ['version_1'] = 1
        ir.protocolVersion ['version_2'] = 1
        ir.protocolVersion ['version_3'] = self.v3_flag
        val = get_charset_negot (ireq)
        charset_name = None
        records_in_charsets = 0
        if val <> None:
            csreq = CharsetNegotReq ()
            csreq.unpack_proposal (val)
            def rand_choose (list_or_none):
                if list_or_none == None or len (list_or_none) == 0:
                    return None
                return random.choice (list_or_none)
            charset_name = rand_choose (csreq.charset_list)
            if charset_name <> None:
                try:
                    codecs.lookup (charset_name)
                except LookupError, l:
                    charset_name = None
            csresp = CharsetNegotResp (
                charset_name,
                rand_choose (csreq.lang_list),
                csreq.records_in_charsets)
            records_in_charsets = csresp.records_in_charsets
            if trace_charset:
                print csreq, csresp
            set_charset_negot (ir, csresp.pack_negot_resp (), self.v3_flag)
            
        optionslist = ['search', 'present', 'delSet', 'scan','negotiation']
        ir.options = Options ()
        for o in optionslist:
            ir.options[o] = 1
            
        ir.preferredMessageSize = 0
        
        ir.exceptionalRecordSize = 0 
        # z9350-2001 3.2.1.1.4, 0 means client should be prepared to accept
        # arbitrarily long messages.
        
        ir.implementationId = implementationId

        ir.implementationName = 'PyZ3950 Test server'
        ir.implementationVersion = impl_vers
        ir.result = 1

        if trace_charset or trace_init:
            print ir
        self.expecting_init = 0
        self.send (('initResponse', ir))
        self.set_codec (charset_name, records_in_charsets)

    def sort (self, sreq):
        sresp = SortResponse ()
        sresp.sortStatus = 0
        self.send (('sortResponse', sresp))
    def delete (self, dreq):
        dresp = DeleteResultSetResponse ()
        dresp.deleteOperationStatus = 0
        self.send (('deleteResultSetResponse', dresp))
    def esrequest (self, esreq):
        print "ES", esreq
        esresp = ExtendedServicesResponse ()
        esresp.operationStatus = ExtendedServicesResponse['operationStatus'].get_num_from_name ('failure')
        self.send (('extendedServicesResponse', esresp))
        
    fn_dict = {'searchRequest': search,
               'presentRequest': present,
               'initRequest' : init,
               'close' : close,
               'sortRequest' : sort,
               'deleteResultSetRequest' : delete,
               'extendedServicesRequest': esrequest}


def run_server (test = 0):
    listen = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    listen.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen.bind (('', DEFAULT_PORT))
    listen.listen (1)
    while 1:
        (sock,addr) = listen.accept ()
        try:
            serv = Server (sock)
            serv.test = test
            serv.run ()
        except:
            (typ, val, tb) = sys.exc_info ()
            if typ == exceptions.KeyboardInterrupt:
                print "kbd interrupt, leaving"
                raise
            print "error %s %s from %s" % (typ, val, addr)
            traceback.print_exc(40)
        sock.close ()
        
def extract_apt (rpnQuery):
    """Takes RPNQuery to AttributePlusTerm"""
    RPNStruct = rpnQuery.rpn
    assert (RPNStruct [0] == 'op')
    operand = RPNStruct [1]
    assert (operand [0] == 'attrTerm')
    return operand [1]


class Client (Conn):
    test = 0

    def __init__ (self, addr, port = DEFAULT_PORT, optionslist = None,
                  charset = None, lang = None, user = None, password = None, 
                  preferredMessageSize = 0x100000, group = None,
                  maximumRecordSize = 0x100000, implementationId = "",
                  implementationName = "", implementationVersion = "",
                  ConnectionError = ConnectionError,
                  ProtocolError = ProtocolError,
                  UnexpectedCloseError = UnexpectedCloseError):
    
        Conn.__init__ (self, ConnectionError = ConnectionError,
                       ProtocolError = ProtocolError,
                       UnexpectedCloseError = UnexpectedCloseError)
        try:
            self.sock.connect ((addr, port))
        except socket.error, val:
            self.sock = None
            raise self.ConnectionError ('socket', str(val))
        try_v3 =  Z3950_VERS == 3

        if (charset and not isinstance(charset, list)):
            charset = [charset]
        if (lang and not isinstance(lang, list)):
            charset = [lang]
        negotiate_charset = charset or lang

        if (user or password or group):
            authentication = (user, password, group)
        else:
            authentication = None

        InitReq = make_initreq (optionslist, authentication = authentication,
                                v3 = try_v3,
                                preferredMessageSize = preferredMessageSize,
                                maximumRecordSize = maximumRecordSize,
                                implementationId = implementationId,
                                implementationName = implementationName,
                                implementationVersion = implementationVersion,
                                negotiate_charset = negotiate_charset)
        if negotiate_charset:
            # languages = ['eng', 'fre', 'enm']
            # Thanne longen folk to looken in catalogues
            # and clerkes for to seken straunge bookes ...
            cnr = CharsetNegotReq (charset, lang, random.choice((0,1,None)))
            if trace_charset:
                print cnr
            set_charset_negot (InitReq, cnr.pack_proposal (), try_v3)

        if trace_init:
            print "Initialize request", InitReq

        self.initresp = self.transact (
            ('initRequest', InitReq), 'initResponse')
        if trace_init:
            print "Initialize Response", self.initresp
        self.v3_flag = self.initresp.protocolVersion ['version_3']
        val = get_charset_negot (self.initresp)
        if val <> None:
            csr = CharsetNegotResp ()
            csr.unpack_negot_resp (val)
            if trace_charset:
                print "Got csr", str (csr)
            self.set_codec (csr.charset, csr.records_in_charsets)

        self.search_results = {}
        self.max_to_request = 20
        self.default_recordSyntax = Z3950_RECSYN_USMARC_ov
    def get_option (self, option_name):
        return self.initresp.options[option_name]
    def transact (self, to_send, expected):
        b = self.encode_ctx.encode (APDU, to_send)
        if print_hex:
            print map (hex, b)
        if self.test:
            print "Internal Testing"
            # a reminder not to leave this switched on by accident
            self.decode_ctx.feed (b)
            decoded = self.read_PDU ()
            print "to_send", to_send, "decoded", decoded
            assert (to_send == decoded)
        if self.sock == None:
            raise self.ConnectionError ('disconnected')
        try:
            self.sock.send (b)
        except socket.error, val:
            self.sock = None
            raise self.ConnectionError('socket', str(val))

        if expected == None:
            return
        pdu = self.read_PDU ()
        (arm, val) = pdu
        if self.test:
            print "Internal Testing 2"
            b = self.encode_ctx.encode (APDU, (arm, val))
            self.decode_ctx.feed (b)
            redecoded = self.read_PDU ()
            if redecoded <> (arm, val):
                print "Redecoded", redecoded
                print "old", (arm, val)
                assert (redecoded == (arm, val))
        if arm == expected: # may be 'close'
            return val
        elif arm == 'close':
            raise self.UnexpectedCloseError (
                "Server closed connection reason %d diag info %s" % \
                (getattr (val, 'closeReason', -1),
                 getattr (val, 'diagnosticInformation', 'None given')))
        else:
            raise self.ProtocolError (
                "Unexpected response from server %s %s " % (expected,
                                                            repr ((arm, val))))
    def set_dbnames (self, dbnames):
        self.dbnames = dbnames
    def search_2 (self, query, rsn = default_resultSetName, **kw):
        # We used to check self.initresp.options['search'], but
        # support for search is required by the standard, and
        # www.cnshb.ru:210 doesn't set the search bit if you negotiate
        # v2, but supports search anyway
        sreq = make_sreq (query, self.dbnames, rsn, **kw)
        recv = self.transact (('searchRequest', sreq), 'searchResponse')
        self.search_results [rsn] = recv
        return recv
    def search (self, query, rsn = default_resultSetName, **kw):
        # for backwards compat
        recv = self.search_2 (('type_1', query), rsn, **kw)
        return recv.searchStatus and (recv.resultCount > 0)
    # If searchStatus is failure, check result-set-status - 
    # -subset - partial, valid results available
    # -interim - partial, not necessarily valid
    # -none - no result set
    # If searchStatus is success, check present-status:
    # - success - OK
    # - partial-1 - not all, access control
    # - partial-2 - not all, won't fit in msg size (but we currently don't ask for
    #               any records in search, shouldn't happen)
    # - partial-3 - not all, resource control (origin)
    # - partial-4 - not all, resource control (target)
    # - failure - no records, nonsurrogate diagnostic.
    def get_count (self, rsn = default_resultSetName):
        return self.search_results[rsn].resultCount
    def delete (self, rsn):
        if not self.initresp.options['delSet']:
            return None
        delreq = DeleteResultSetRequest ()
        delreq.deleteFunction = 0 # list
        delreq.resultSetList = [rsn]
        return self.transact (('deleteResultSetRequest', delreq),
                              'deleteResultSetResponse')
    def present (self, rsn= default_resultSetName, start = None,
                 count = None, recsyn = None, esn = None):
        # don't check for support in init resp: see search for reasoning

        # XXX Azaroth 2004-01-08. This does work when rs is result of sort.
        try:
            sresp = self.search_results [rsn]
            if start == None:
                start = sresp.nextResultSetPosition
                if count == None:
                    count = sresp.resultCount
                    if self.max_to_request > 0:
                        count = min (self.max_to_request, count)
        except:
            pass
        if recsyn == None:
            recsyn = self.default_recordSyntax
        preq = PresentRequest ()
        preq.resultSetId = rsn
        preq.resultSetStartPoint = start
        preq.numberOfRecordsRequested = count
        preq.preferredRecordSyntax = recsyn
        if esn <> None:
            preq.recordComposition = ('simple', esn)
        return self.transact (('presentRequest', preq), 'presentResponse')
    def scan (self, query, **kw):
        sreq = ScanRequest ()
        sreq.databaseNames = self.dbnames
        assert (query[0] == 'type_1' or query [0] == 'type_101')
        sreq.attributeSet = query[1].attributeSet
        sreq.termListAndStartPoint = extract_apt (query[1])
        sreq.numberOfTermsRequested = 20 # default
        for (key, val) in kw.items ():
            setattr (sreq, key, val)

        return self.transact (('scanRequest', sreq), 'scanResponse')
    def close (self):
        close = Close ()
        close.closeReason = 0
        close.diagnosticInformation = 'Normal close'
        try:
            rv =  self.transact (('close', close), 'close')
        except self.ConnectionError:
            rv = None
        if self.sock <> None:
            self.sock.close ()
            self.sock = None
        return rv


def mk_compound_query ():
    aelt1 = AttributeElement (attributeType = 1,
                              attributeValue = ('numeric',4))
    apt1 = AttributesPlusTerm ()
    apt1.attributes = [aelt1]
    apt1.term = ('general', '1066')
    aelt2 = AttributeElement (attributeType = 1,
                              attributeValue = ('numeric', 1))
    apt2 = AttributesPlusTerm ()
    apt2.attributes = [aelt2]
    apt2.term = ('general', 'Sellar')
    myrpnRpnOp = RpnRpnOp ()
    myrpnRpnOp.rpn1 = ('op', ('attrTerm', apt1))
    myrpnRpnOp.rpn2 = ('op', ('attrTerm', apt2))
    myrpnRpnOp.op = ('and', None)
    rpnq = RPNQuery (attributeSet = Z3950_ATTRS_BIB1_ov)
    rpnq.rpn = ('rpnRpnOp', myrpnRpnOp)
    return rpnq

def mk_simple_query (title):
    aelt1 = AttributeElement (attributeType = 1,
                              attributeValue = ('numeric', 1003))
    apt1 = AttributesPlusTerm ()
    apt1.attributes = [aelt1]
    apt1.term = ('general', title) # XXX or should be characterString, not general, but only when V3.
    rpnq = RPNQuery (attributeSet = Z3950_ATTRS_BIB1_ov)
    rpnq.rpn = ('op', ('attrTerm', apt1))
    return rpnq

def_host = 'LC'

host_dict = {'BIBSYS': ('z3950.bibsys.no', 2100, 'BIBSYS'),
             'YAZ': ('127.0.0.1', 9999, 'foo'),
             'LCTEST' :  ('ilssun2.loc.gov', 7090, 'Voyager'),
             'LC' : ('z3950.loc.gov', 7090, 'Voyager'),
             'NLC' : ('amicus.nlc-bnc.ca', 210, 'NL'),
             'BNC' : ('amicus.nlc-bnc.ca', 210, 'NL'),
             # On parle franc,ais aussi.
             'LOCAL': ('127.0.0.1', 9999, 'Default'),
             'LOCAL2': ('127.0.0.1', 2101, 'foo'),
             'BL' :('blpcz.bl.uk', 21021, 'BLPC-ALL'),
             'BELLLABS' : ('z3950.bell-labs.com', 210, 'books'),
             'BIBHIT' : ('www.bibhit.dk', 210, 'Default'),
             'YALE': ('webpac.library.yale.edu', 210, 'YALEOPAC'),
             'OXFORD': ('library.ox.ac.uk', 210, 'ADVANCE'),
             'OVID': ('z3950.ovid.com', 2213, 'pmed'), # scan only
             'UC':   ('ipac.lib.uchicago.edu', 210, 'uofc'),
             'KUB' : ('dbiref.kub.nl', 1800, 'jel'),
             'INDEXDATA' : ('muffin.indexdata.dk', 9004, 'thatt')}
# last two are Zthes servers.

if __name__ == '__main__':
    optlist, args = getopt.getopt (sys.argv[1:], 'e:sh:tc:l:')
    server = 0
    host = def_host
    test = 0
    charset_list = None
    lang_list = None
    for (opt, val) in optlist:
        if opt == '-s':
            server = 1
        elif opt == '-h':
            host = val
        elif opt == '-t':
            test = 1
        elif opt  == '-e':
            out_encoding = val
        elif opt == '-c':
            charset_list = val.split (',')
        elif opt == '-l':
            lang_list = val.split (',')
    if server:
        run_server (test)

    host = host.upper ()
    (name, port, dbname) = host_dict.get (host, host_dict[def_host])
    cli = Client (name, port, charset = charset_list,
                  lang = lang_list)
    cli.test = test
    cli.set_dbnames ([dbname])
    print "Starting search"
#    rpnq = mk_simple_query ('Perec, Georges')
#    rpnq = mk_simple_query ('Johnson, Kim')
    rpnq = mk_compound_query ()
    if cli.search (rpnq, smallSetUpperBound = 0, mediumSetPresentNumber = 0,
                   largeSetLowerBound = 1):
        disp_resp (cli.present (recsyn = Z3950_RECSYN_USMARC_ov))
    else:
        print "Not found"
    print "Deleting"
    cli.delete (default_resultSetName)
    cli.delete ('bogus')
    print "Closing"
    try:
        cli.close ()
    except ConnectionError:
        # looks like LC, at least, sends a FIN on receipt of Close PDU
        # guess we should check for gracefullness of close, and complain
        # if not.
        pass

