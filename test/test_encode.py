"""
Encode a bunch of z39.50 PDUs to make sure we can do so properly.
"""
import os
from PyZ3950.z3950_2001 import *
from PyZ3950.zdefs import make_initreq
from PyZ3950.asn1 import encode


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_init_req():
     initreq = make_initreq(some stuff)
     actual_data = encode(APDU, ('InitRequest', initreq))

