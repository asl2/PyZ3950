#!/usr/bin/env python3

"""A Z39.50 interface to Amazon, using Twisted
(http://www.twistedmatrix.com, I tested with 1.0.5) and Mark Pilgrim's
pyamazon (http://www.diveintomark.org/projects/pyamazon/).  Note that
you'll have to obtain your own Amazon license key, and will be
responsible for complying with Amazon's terms of use (I think that
setting up a publicly accessible gateway would not comply).

This needs a whole lot of work before it's production-quality,
mostly (but not exclusively) Z39.50 error-handling, and better
integration into the Twisted service framework."""


from twisted.internet import reactor, protocol
from twisted.web.client import getPage
from xml.dom import minidom

from PyZ3950 import zdefs, asn1
import amazon

def start_amazon_query (query, callback, errback):
    url = amazon.buildURL ("PowerSearch", query, "books",
                           "heavy", # or map B esn to lite, F to "heavy"
                           1, # page number
                           amazon.LICENSE_KEY)
    getPage (url).addCallbacks (
        callback = lambda page: parse_amazon_resp (page, callback, errback),
        errback = errback)
    
def parse_amazon_resp (data, callback, errback):
    print(data)
    xmldoc = minidom.parseString (data)
    data = amazon.unmarshal (xmldoc).ProductInfo
    if hasattr(data, 'ErrorMsg'):
        errback (data.ErrorMsg)
    else:
        callback (data.Details)

def r_to_a_attr (attrs):
    assert len (attrs) == 1
    attr = attrs [0]
    assert attr.attributeType == 1  # 'use' attribute
    typ, val = attr.attributeValue
    assert typ == 'numeric'
    return {1: 'Author',
            4: 'Title',
            7: 'ISBN',
            1003: 'Title',
            1016: 'Keyword'}.get (val)

def rpn_q_to_amazon (query):
    typ, rpn_query = query
    assert typ in ('type_1', 'type_2')
    def aux (q):
        # ignore attributeSet
        typ, val = q
        if typ == 'op':
            assert val [0] == 'attrTerm'
            val = val [1]
            amazon_attr = r_to_a_attr (val.attributes)
            return "%s: %s" % (amazon_attr, val.term[1]) # XXX ignore term type
        else:
            a1 = aux (val.rpn1)
            a2 = aux (val.rpn2)
            r_op = val.op [0]
            assert val.op [1] == None
            if r_op == 'and_not':
                r_op = 'and not'
            return "(%s) %s (%s)" % (a1, r_op, a2)

    return aux (rpn_query.rpn)

class Z3950Server(protocol.Protocol):
    inited = 0
    def init (self):
        self.decode_ctx = asn1.IncrementalDecodeCtx (zdefs.APDU)
        self.encode_ctx = asn1.Ctx ()
        self.result_sets = {}
        self.inited = 1
    def ensure_init (self):
        if not self.inited:
            self.init ()
        
    def connectionLost (self, reason):
        self.ensure_init ()
        self.transport.loseConnection ()
        print("lost conn for reason", reason)
    def handle_error (self, errobj):
        raise errobj
    def dataReceived (self, data):
        self.ensure_init ()
        try:
            self.decode_ctx.feed (list(map (ord, data)))
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
    def process_initRequest (self, val):
        ir = zdefs.InitializeResponse ()
        ir.protocolVersion = zdefs.ProtocolVersion ()
        ir.protocolVersion ['version_1'] = 1
        ir.protocolVersion ['version_2'] = 1
        ir.options = zdefs.Options ()
        ir.options ['search'] = 1
        ir.options ['present'] = 1
        ir.preferredMessageSize = 0
        ir.exceptionalRecordSize = 0
        ir.implementationId = zdefs.implementationId
        ir.implementationName = 'PyZ3950 Z39.50 -> Amazon gateway'
        ir.implementationVersion = zdefs.impl_vers + ' (gw 0.1)'
        ir.result = 1
        self.send_PDU ('initResponse', ir)
    def process_searchRequest (self, sreq):
        def success (val):
            print("val len", len (val))
            try:
                def strify_dict (bag):
                    d = bag.__dict__
                    def represent (s):
                        if isinstance (s, str):
                            return s
                        if isinstance (s, amazon.Bag):
                            return strify_dict (s)
                        if isinstance (s, str):
                            try:
                                return s.encode ('ascii')
                            except UnicodeError:
                                pass
                        return repr (s) # Unicode, and catch-all

                    return ["%s: %s" % (t[0], represent (t[1]))
                            for t in list(d.items ())]
                string_list = ["\n".join (strify_dict (x)) for x in val]
                self.result_sets [sreq.resultSetName] = string_list
                print("creating resp", repr (sreq.resultSetName), self, self.result_sets)
                sresp = zdefs.SearchResponse ()
                print("resp created")
                sresp.resultCount = len (string_list)
                print("result count", sresp.resultCount)
                sresp.numberOfRecordsReturned = 0
                sresp.nextResultSetPosition = 1
                print("setting search status")
                sresp.searchStatus = 1
                print("setting presentStatus")
                sresp.presentStatus = zdefs.PresentStatus.get_num_from_name (
                    'success')
                print("about to send")

                self.send_PDU ('searchResponse', sresp)
            except Exception as e:
                print("Exception:", e)
                raise
                
            
        def failure (str):
            print("failed", str)
            sresp = zdefs.SearchResponse ()
            sresp.resultCount = 0
            sresp.numberOfRecordsReturned = 0
            sresp.nextResultSetPosition = 1
            sresp.searchStatus = 0
            self.send_PDU ('searchResponse', sresp)

        amazon_query = rpn_q_to_amazon (sreq.query)
        start_amazon_query (amazon_query, success, failure)
    def format_records (self, start, count, res_set, rec_syn):
        l = []
        for i in range (start - 1, start + count - 1):
            elt = res_set[i]
            elt_external = asn1.EXTERNAL ()
            elt_external.direct_reference = zdefs.Z3950_RECSYN_SUTRS_ov
            elt_external.encoding = ('single-ASN1-type', elt)
            n = zdefs.NamePlusRecord ()
            n.name = 'foo' # XXX
            n.record = 'retrievalRecord', elt_external
            l.append (n)
        return l

    def process_presentRequest (self, preq):
        presp = zdefs.PresentResponse ()
        print("accessing", repr (preq.resultSetId), self.result_sets)
        res_set = self.result_sets [preq.resultSetId]
        presp.numberOfRecordsReturned = preq.numberOfRecordsRequested
        presp.nextResultSetPosition = preq.resultSetStartPoint + \
                                      preq.numberOfRecordsRequested
        presp.presentStatus = zdefs.PresentStatus.get_num_from_name ('success')
        presp.records = ('responseRecords',
                         self.format_records (preq.resultSetStartPoint,
                                              preq.numberOfRecordsRequested,
                                              res_set,
                                              preq.preferredRecordSyntax))
        self.send_PDU ('presentResponse', presp)

    def process_close (self, creq):
        close = zdefs.Close ()
        close.closeReason = zdefs.CloseReason.get_num_from_name (
            'responseToPeer')
        self.send_PDU ('close', close)
        self.transport.loseConnection ()
        
if __name__ == '__main__':
    if 0:
        from PyZ3950 import z3950
        print(rpn_q_to_amazon (
            ('type_1', z3950.mk_simple_query ('Among the gently mad'))))
        print(rpn_q_to_amazon (('type_1', z3950.mk_compound_query ())))
    else:
        amazon.setLicense (amazon.getLicense ())
        factory = protocol.Factory ()
        factory.protocol = Z3950Server
        reactor.listenTCP (2100, factory)
        reactor.run ()
