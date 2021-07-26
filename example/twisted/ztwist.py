#!/usr/bin/env python

"""A Z39.50 / Twisted interface. """
from __future__ import print_function

from twisted.internet import reactor, protocol
from twisted.internet import defer

from PyZ3950 import zdefs, asn1, zoom, oids

class ErrRaiser:
    def raise_err (self, num, addtlinfo, eb):
        err = zoom.Bib1Err (num, None, addtlinfo) # middle 'None' is unused
        eb (err)
        raise err

class AttribXlate(ErrRaiser):

    """Utility class for supporting simple v2 queries, Use attributes
    only.  You must inherit from this class, provide term_xlate and
    combiner methods which translate to your data structures, and set
    self.oid appropriately.  You can also override translate_attr and
    translate_term if the attribute/term type restrictions are
    problematic for you."""

    def __init__ (self, eb):
        self.eb = eb
        
    def translate (self, query):
        try:
            (qtyp, qval) = query
            if qtyp != 'type_1':
                self.raise_err (107, qtyp, self.eb)
            if qval.attributeSet != self.oid:
                self.raise_err (123, str (qval.attributeSet), self.eb)
            return self.translate_rpn (qval.rpn)
        except zoom.Bib1Err as e:
            return None
    def translate_attr (self, attrs):
        """Checks attributes, and translates them to whatever the term_xlate
        callback expects.  Override this if you want to handle attribute
        combinations, attributes other than BIB-1 USE attributes,
        non-numeric attributes, etc."""
        if (len (attrs) > 1 or
            (getattr (attrs[0],'attributeSet',self.oid) != self.oid)):
            self.raise_err (1024, str (attrs), self.eb)
        if attrs [0].attributeType != 1: # use attribute
            self.raise_err (116, str (attrs), self.eb) # or 117-120
        (atyp, aval) = attrs[0].attributeValue
        if atyp != 'numeric':
            self.raise_err (113, str (attrs), self.eb)
        return aval
    def translate_term (self, term):
        """Translates term to whatever the term_xlate callback expects.
        Override this to handle term types other than 'general'."""
        (ttyp, tval) = term
        if ttyp != 'general':
            self.raise_err (229, str (term), self.eb)
        return tval
        
    def translate_rpn (self, rpn):
        (typ, val) = rpn
        if typ == 'op':
            (operandtyp, op) = val
            if operandtyp == 'attrTerm':
                aval = self.translate_attr (op.attributes)
                tval = self.translate_term (op.term)
                return self.term_xlate (aval, tval)
            elif operandtyp == 'resultSet' or operandtyp == 'resultAttr':
                self.raise_err (18, str (rpn), self.eb)
        else:
            operator = val.op[0] # [1] is always NULL, translated to None
            r1 = self.translate_rpn (val.rpn1)
            r2 = self.translate_rpn (val.rpn2)
            return self.combiner (operator, r1, r2)

class Z3950Server(protocol.Protocol, ErrRaiser):
    def __init__ (self, *args, **kw):
        raise "Must subclass and set self.searcher dictionary"
    def connectionMade (self):
        self.decode_ctx = asn1.IncrementalDecodeCtx (zdefs.APDU)
        self.encode_ctx = asn1.Ctx ()
        self.result_sets = {}
        self.close_sent = 0
        self.closed = 0
    def connectionLost (self, reason):
        self.transport.loseConnection ()
        if not self.closed:
            print("lost conn for reason", reason)
    def handle_error (self, errobj):
        raise errobj
    def dataReceived (self, data):
        try:
            self.decode_ctx.feed (map (ord, data))
        except asn1.BERError as val:
            self.handle_error (val)
            return
        while self.decode_ctx.val_count () > 0:
            self.process_PDU (self.decode_ctx.get_first_decoded ())
    def process_PDU (self, PDU):
        arm, val = PDU
        fn = getattr (self, 'process_' + arm)
        fn (val)
    def send_PDU (self, arm, val):
        b = self.encode_ctx.encode (zdefs.APDU, (arm, val))
        self.transport.write ("".join (map (chr, b)))
    def get_implementation_name (self):
        return 'PyZ3950/Twisted Z39.50 server'
    def get_implementation_ver (self):
        return zdefs.impl_vers + ' (gw 0.1)'
    def set_diagrec (self, err, resp):
        diagrec = zdefs.DefaultDiagFormat ()
        diagrec.diagnosticSetId = oids.Z3950_DIAG_BIB1_ov
        if isinstance (err, zoom.Bib1Err):
            diagrec.condition = err.condition
            diagrec.addinfo = ('v3Addinfo', err.addtlInfo)
        else:
            diagrec.condition = 1
            diagrec.addinfo = str (err)
        if self.v3:
            diagrecs = [('defaultFormat', diagrec)]
            resp.records = ('multipleNonSurDiagnostics',
                                         diagrecs)
        else:
            resp.records = ('nonSurrogateDiagnostic',
                                         diagrec)
        
    def process_initRequest (self, val):
        ir = zdefs.InitializeResponse ()
        ir.protocolVersion = zdefs.ProtocolVersion ()
        ir.protocolVersion ['version_1'] = 1
        ir.protocolVersion ['version_2'] = 1
        self.v3 = 0
        ir.options = zdefs.Options ()
        ir.options ['search'] = 1
        ir.options ['present'] = 1
        ir.preferredMessageSize = 0
        ir.exceptionalRecordSize = 0
        ir.implementationId = zdefs.implementationId
        ir.implementationName = self.get_implementation_name ()
        ir.implementationVersion = self.get_implementation_ver ()
        ir.result = 1
        self.send_PDU ('initResponse', ir)
        
    def process_searchRequest (self, sreq):
        def cb (l):
            self.result_sets [sreq.resultSetName] = l
            sresp = zdefs.SearchResponse ()
            sresp.resultCount = len (l)
            sresp.numberOfRecordsReturned = 0
            sresp.nextResultSetPosition = 1
            sresp.searchStatus = 1
            sresp.presentStatus = zdefs.PresentStatus.get_num_from_name (
                'success')
            self.send_PDU ('searchResponse', sresp)
            
        def eb (err):
            sresp = zdefs.SearchResponse ()
            sresp.searchStatus = 0 # boolean
            sresp.numberOfRecordsReturned = 1
            sresp.resultCount = 0
            sresp.nextResultSetPosition = 0
            self.set_diagrec (err, sresp)

            self.send_PDU ('searchResponse', sresp)
        try:
            if (self.result_sets.has_key (sreq.resultSetName) and
                sreq.replaceIndicator == 0):
                self.raise_err (21, sreq.resultSetName, eb)
            searcher = self.get_searcher (sreq.databaseNames, eb)
            if searcher is not None:
                searcher.search (sreq.query, cb, eb)
        except zoom.Bib1Err as e:
            pass


    def get_searcher (self, dbnames, eb):
        """Override this to support multiple-db searches by creating
        an appropriate multiplexing searcher."""
        if len (dbnames) != 1:
            self.raise_err (111, str (dbnames), eb)
            return None
        searcher = self.searcher.get (dbnames[0], None)
        if searcher == None:
            self.raise_err (109, str (dbnames), eb)
            return None
        return searcher
    def process_presentRequest (self, preq):
        # XXX it looks to me as if it's erroneous to request more
        # records than the search response indicated are available.
        # return bib-1 error 13 in this case, rather than a partial set
        # of records.  See http://lcweb.loc.gov/z3950/agency/markup/04.html,
        # 3.2.3.1.8.
        
        class PresentInfo:
            """The weird structure here (with the next() method) is
            for integration with Twisted."""




            def __init__ (self, server, res, preq):
                self.presp = zdefs.PresentResponse ()
                self.server = server
                self.rec_end = (preq.resultSetStartPoint +
                           preq.numberOfRecordsRequested) - 1
                if self.rec_end > len (res):
                    self.fail (13)
                    return
                self.esn = None
                gESN = 'genericElementSetName'
                def_esn = (gESN, 'B')
                (esntyp, esn) = getattr (preq, 'recordComposition',
                                         ('simple', def_esn))
                if esntyp == 'simple':
                    (typ2, esn2) = esn
                    if typ2 == gESN:
                        self.esn = esn2
                if self.esn == None:
                    self.fail (24, esntyp)
                    return
                
                self.presp.numberOfRecordsReturned = preq.numberOfRecordsRequested
                self.presp.nextResultSetPosition = self.rec_end
                self.count = preq.resultSetStartPoint - 2
                # -1 b/c we increment right away in next, -1 because it's
                # one-based, not zero-based
                self.res = res
                self.recs = []
                self.syntax = preq.preferredRecordSyntax
                self.next ()
            def next (self, rec = None):
                self.count = self.count + 1
                if rec is not None:
                    self.recs.append (rec)
                if self.count == self.rec_end:
                    self.finish ()
                else:
                    rec = self.res [self.count]
                    rec[0].format_one (rec[1], self.esn,
                                       self.syntax, self.next)
                                    
            def finish (self):
                self.presp.records = ('responseRecords',
                                      self.recs)
                self.presp.presentStatus = zdefs.PresentStatus.get_num_from_name ('success') 
                self.server.send_PDU ('presentResponse', self.presp)
                
            def fail (self, errno, reason = ''):
                self.presp.nextResultSetPosition = 0
                self.presp.presentStatus = zdefs.PresentStatus.get_num_from_name ('failure')
                self.presp.numberOfRecordsReturned = 0
                self.server.set_diagrec (zoom.Bib1Err (errno, '', reason),
                                         self.presp)
                self.server.send_PDU ('presentResponse', self.presp)
        pinfo = PresentInfo (self, self.result_sets [preq.resultSetId], preq)

    def process_close (self, val):
        self.closed = 1
        if not self.close_sent:
            my_close = zdefs.Close ()
            my_close.closeReason = zdefs.CloseReason.get_num_from_name (
                'responseToPeer')
            self.send_PDU ('close', my_close)
        self.transport.loseConnection ()


# for sample usage, see textsearch.py in this directory.
        

    










