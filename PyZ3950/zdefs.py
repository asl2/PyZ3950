#!/usr/bin/env python

import codecs

from PyZ3950.z3950_2001 import *
from PyZ3950.oids import *

    
asn1.register_oid (Z3950_RECSYN_GRS1, GenericRecord)
asn1.register_oid (Z3950_RECSYN_SUTRS, asn1.GeneralString)
asn1.register_oid (Z3950_RECSYN_EXPLAIN, Explain_Record)
asn1.register_oid (Z3950_RECSYN_OPAC, OPACRecord)

asn1.register_oid (Z3950_ES_PERSISTRS, PersistentResultSet)
asn1.register_oid (Z3950_ES_PERSISTQRY, PersistentQuery)
asn1.register_oid (Z3950_ES_PERIODQRY, PeriodicQuerySchedule)
asn1.register_oid (Z3950_ES_ITEMORDER, ItemOrder)
asn1.register_oid (Z3950_ES_DBUPDATE, Update)
asn1.register_oid (Z3950_ES_DBUPDATE_REV_1, Update_updrev1)
asn1.register_oid (Z3950_ES_EXPORTSPEC, ExportSpecification)
asn1.register_oid (Z3950_ES_EXPORTINV, ExportInvocation)


asn1.register_oid (Z3950_USR_SEARCHRES1, SearchInfoReport)
asn1.register_oid (Z3950_USR_INFO1, OtherInformation)
asn1.register_oid (Z3950_NEG_CHARSET3, CharSetandLanguageNegotiation_3)
asn1.register_oid (Z3950_USR_PRIVATE_OCLC_INFO, OCLC_UserInformation)

# below here is subject to change without notice, as I try to
# figure out the appropriate balance between convenience and flexibility

trace_charset = 0

impl_vers = "1.0 beta" # XXX
implementationId = 'PyZ39.50 - contact asl2@pobox.com' # haven't been assigned an official id, apply XXX

def make_attr(set=None, atype=None, val=None, valType=None):
    ae = AttributeElement()
    if (set <> None):
        ae.attributeSet = set
    ae.attributeType = atype
    if (valType == 'numeric' or (valType == None and isinstance(val, int))):
        ae.attributeValue = ('numeric', val)
    else:
        cattr = AttributeElement['attributeValue']['complex']()
        if (valType == None):
            valType = 'string'
        cattr.list = [(valType, val)]
        ae.attributeValue = ('complex', cattr)
    return ae

# This list is needed to support recordsInSelectedCharSets == 0 when
# character set negotiation is in effect.  The reason we don't
# just iterate over Z3950_RECSYN is that many of those are carried
# in OCTET STRINGs, and thus immune to negotiation; but maybe we should
# anyway.

retrievalRecord_oids = [
    Z3950_RECSYN_EXPLAIN_ov,
    Z3950_RECSYN_SUTRS_ov,
    Z3950_RECSYN_OPAC_ov,
    Z3950_RECSYN_SUMMARY_ov,
    Z3950_RECSYN_GRS1_ov,
    Z3950_RECSYN_ES_ov,
    Z3950_RECSYN_FRAGMENT_ov,
    Z3950_RECSYN_SQL_ov]


def register_retrieval_record_oids (ctx, new_codec_name = 'ascii'):
    new_codec = codecs.lookup (new_codec_name)
    def switch_codec ():
        ctx.push_codec ()
        ctx.set_codec (asn1.GeneralString, new_codec)
    for oid in retrievalRecord_oids:
        ctx.register_charset_switcher (oid, switch_codec)

iso_10646_oid_to_name = {
    UNICODE_PART1_XFERSYN_UCS2_ov : 'utf-16', # XXX ucs-2 should differ from utf-16, in that ucs-2 forbids any characters not in the BMP, whereas utf-16 is a 16-bit encoding which encodes those characters into multiple 16-bit units
   
#    UNICODE_PART1_XFERSYN_UCS4_ov : 'ucs-4', # XXX no python support for this encoding?
    UNICODE_PART1_XFERSYN_UTF16_ov : 'utf-16',
    UNICODE_PART1_XFERSYN_UTF8_ov : 'utf-8'
    }

def try_get_iso10646_oid (charset_name):
    for k,v in iso_10646_oid_to_name.iteritems ():
        if charset_name == v:
            return k
    # XXX note that we don't know which of {UCS2, UTF16} oids we'll
    # get from this.

def asn_charset_to_name (charset_tup):
    if trace_charset:
        print "asn_charset_to_name", charset_tup
    charset_name = None
    (typ, charset) = charset_tup
    if typ == 'iso10646':
        charset_name = iso_10646_oid_to_name.get (charset.encodingLevel,
                                        None)
    elif typ == 'private':
        (spectyp, val) = charset
        if spectyp == 'externallySpecified':
            oid = getattr (val, 'direct_reference', None)
            if oid == Z3950_NEG_PRIVATE_INDEXDATA_CHARSETNAME_ov:
                enctyp, encval = val.encoding
                if enctyp == 'octet-aligned':
                    charset_name = encval
    if trace_charset:
        print "returning charset", charset_name
    return charset_name


def charset_to_asn (charset_name):
    oid = try_get_iso10646_oid (charset_name)
    if oid <> None:
        iso10646 = Iso10646_3 ()
        iso10646.encodingLevel = oid
        return ('iso10646', iso10646)
    else:
        ext = asn1.EXTERNAL ()
        ext.direct_reference = Z3950_NEG_PRIVATE_INDEXDATA_CHARSETNAME_ov
        ext.encoding = ('octet-aligned', charset_name)
        return ('private', ('externallySpecified', ext))

class CharsetNegotReq:
    def __init__ (self, charset_list = None, lang_list = None,
                  records_in_charsets = None):
        """charset_list is a list of character set names, either ISO10646
(UTF-8 or UTF-16), or private.  We support Index Data's semantics
for private character sets (see
http://www.indexdata.dk/pipermail/yazlist/2003-March/000504.html), so
you can pass any character set name for which Python has a codec installed
(but please don't use rot13 in production).  Note that there should be
at most one of each of (ISO10646, private).  (No, I don't know why, but
it says so in the ASN.1 definition comments.)

lang_list is a list of language codes, as defined in ANSI Z39.53-1994
(see, e.g., http://xml.coverpages.org/nisoLang3-1994.html).

records_in_charsets governs whether charset negotiation applies to
records, as well.)

Any of these parameters can be None, since the corresponding
elements in the ASN.1 are OPTIONAL.
"""
        self.charset_list = charset_list
        self.lang_list = lang_list
        self.records_in_charsets = records_in_charsets
    def __str__ (self):
        return "Charset negot request %s %s %s" % (
            str (self.charset_list), str (self.lang_list),
            str (self.records_in_charsets))
    def pack_proposal (self):
        origin_prop = OriginProposal_3 ()
        if self.charset_list <> None:
            proposedCharSets = []
            for charset_name in self.charset_list:
                proposedCharSets.append (charset_to_asn (charset_name))

            origin_prop.proposedCharSets = proposedCharSets
        if self.lang_list <> None:
            origin_prop.proposedlanguages = self.lang_list
        if self.records_in_charsets <> None:
            origin_prop.recordsInSelectedCharSets = (
                self.records_in_charsets)
        return ('proposal', origin_prop)
    def unpack_proposal (self, csn):
        (tag, proposal) = csn
        assert (tag == 'proposal')
        pcs = getattr (proposal, 'proposedCharSets', None)
        if pcs <> None:
            if trace_charset:
                print "pcs", pcs
            self.charset_list = []

            for charset in pcs:
                charset_name = asn_charset_to_name (charset)
                if charset_name <> None:
                    self.charset_list.append (charset_name)

        lang = getattr (proposal, 'proposedlanguages', None)
        if lang <> None:
            self.lang_list = lang
        self.records_in_charsets = getattr (proposal,
                                            'recordsInSelectedCharSets', None)


class CharsetNegotResp:
    def __init__ (self, charset = None, lang = None,
                  records_in_charsets = None):
        self.charset = charset
        self.lang = lang
        self.records_in_charsets = records_in_charsets
    def __str__ (self):
        return "CharsetNegotResp: %s %s %s" % (
            str (self.charset), str (self.lang),
            str (self.records_in_charsets))
    def unpack_negot_resp (self, neg_resp):
        typ, val = neg_resp
        assert (typ == 'response')
        self.charset = None
        scs = getattr (val, 'selectedCharSets', None)
        if scs <> None:
            self.charset = asn_charset_to_name (scs)
        self.lang = getattr (val, 'selectedLanguage', None)
        self.records_in_charsets = getattr (
            val, 'recordsInSelectedCharSets', None)
    def pack_negot_resp (self):
        resp = TargetResponse_3 ()
        if self.charset <> None:
            resp.selectedCharSets = charset_to_asn (self.charset)
        if self.lang <> None:
            resp.selectedLanguage = self.lang
        if self.records_in_charsets <> None:
            resp.recordsInSelectedCharSets = self.records_in_charsets
        return ('response', resp)

    
def get_charset_negot (init): # can be passed either InitializeRequest or InitializeResponse
    if trace_charset:
        print init
    if not init.options ['negotiation']:
        return None
    otherInfo = []
    if hasattr (init, 'otherInfo'):
        otherInfo = init.otherInfo
    elif hasattr (init, 'userInformationField'):
        ui = init.userInformationField
        if ui.direct_reference == Z3950_USR_INFO1_ov:
            (enctype, otherInfo) = ui.encoding

    for oi in otherInfo:
        if trace_charset:
                print oi
        (typ, val) =  oi.information
        if typ == 'externallyDefinedInfo':
            if val.direct_reference == Z3950_NEG_CHARSET3_ov:
                (typ, val) = val.encoding
                if typ == 'single-ASN1-type':
                    return val
                    
    return None


def set_charset_negot (init, val, v3_flag):
    # again, can be passed either InitializeRequest or Response
    negot = asn1.EXTERNAL ()
    negot.direct_reference = Z3950_NEG_CHARSET3_ov
    negot.encoding= ('single-ASN1-type', val)
    OtherInfoElt = OtherInformation[0]
    oi_elt = OtherInfoElt ()
    oi_elt.information = ('externallyDefinedInfo', negot)
    other_info = [oi_elt]
    if trace_charset:
        print v3_flag, oi_elt

    if v3_flag:
        init.otherInfo = other_info
    else:
        ui = asn1.EXTERNAL ()

        ui.direct_reference = Z3950_USR_INFO1_ov
        ui.encoding = ('single-ASN1-type', other_info) # XXX test this
        # see http://lcweb.loc.gov/z3950/agency/defns/user-1.html
        init.userInformationField = ui


def_msg_size = 0x10000

# rethink optionslist.  Maybe we should just turn on all the
# bits the underlying code supports?  We do need to be able to
# turn off multiple result sets for testing (see tests/test2.py),
# but that doesn't have to be the default.
def make_initreq (optionslist = None, authentication = None, v3 = 0,
                  negotiate_charset = 0, preferredMessageSize = 0x100000,
                  maximumRecordSize = 0x100000, implementationId = "",
                  implementationName = "", implementationVersion = ""):

    # see http://lcweb.loc.gov/z3950/agency/wisdom/unicode.html
    InitReq = InitializeRequest ()
    InitReq.protocolVersion = ProtocolVersion ()
    InitReq.protocolVersion ['version_1'] = 1
    InitReq.protocolVersion ['version_2'] = 1
    InitReq.protocolVersion ['version_3'] = v3
    InitReq.options = Options ()
    if optionslist <> None:
        for o in optionslist:
            InitReq.options[o] = 1
    InitReq.options ['search'] = 1
    InitReq.options ['present'] = 1
    InitReq.options ['delSet'] = 1
    InitReq.options ['scan'] = 1
    InitReq.options ['sort'] = 1
    InitReq.options ['extendedServices'] = 1
    InitReq.options ['dedup'] = 1
    InitReq.options ['negotiation'] = negotiate_charset # XXX can negotiate other stuff, too

# Preferred and Exceptional msg sizes are pretty arbitrary --
# we dynamically allocate no matter what
    InitReq.preferredMessageSize = preferredMessageSize
    InitReq.exceptionalRecordSize = maximumRecordSize

    if (implementationId):
        InitReq.implementationId = implementationId
    else:
        InitReq.implementationId = impl_id
    if (implementationName):
        InitReq.implementationName = implementationName
    else:
        InitReq.implementationName = 'PyZ3950'
    if (implementationVersion):
        InitReq.implementationVersion = implementationVersion
    else:
        InitReq.implementationVersion = impl_vers

    if authentication <> None:
        class UP: pass
        up = UP ()
        upAttrList = ['userId', 'password', 'groupId']
        for val, attr in zip (authentication, upAttrList): # silently truncate
            if val <> None:
                setattr (up, attr, val)
        InitReq.idAuthentication = ('idPass', up)

    return InitReq

def make_sreq (query, dbnames, rsn, **kw):
    sreq = SearchRequest ()
    sreq.smallSetUpperBound = 0
    sreq.largeSetLowerBound = 1
    sreq.mediumSetPresentNumber = 0
# as per http://lcweb.loc.gov/z3950/lcserver.html, Jun 07 2001,
# to work around Endeavor bugs in 1.13
    sreq.replaceIndicator = 1
    sreq.resultSetName = rsn
    sreq.databaseNames = dbnames
    sreq.query = query
    for (key, val) in kw.items ():
        setattr (sreq, key, val)
    return sreq
