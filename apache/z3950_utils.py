
from PyZ3950 import asn1
from PyZ3950.oids import *
from PyZ3950.z3950_2001 import *
from PyZ3950.zdefs import *

def negotiateCharSet(req, resp):
    if hasattr (req, 'otherInfo'):
        for oi in req.otherInfo:
            (typ, val) =  oi.information
            if (typ == 'externallyDefinedInfo' and val.direct_reference == Z3950_NEG_CHARSET3_ov):
                (typ, val) = val.encoding
                if typ == 'single-ASN1-type':
                    set_charset (resp, make_target_resp (val), 1)
    return resp

def decodeExtendedServices(req):
    # This stuff is page 61 and 227 for the ASN1
    # function: 1 create, 2 delete, 3 modify
    # waitAction: 1 wait, 2 waitIfPossible, 3 dontWait, 4 dontReturnPackage

    esoids = oids['Z3950']['ES']
    tsp = req.taskSpecificParameters
    package = req.packageType

    if (req.packageType == esoids['PERSISTRS']['oid']):
        pass
    
