"""
Decode a whole bunch of z3950 PDUs
"""
import os
from PyZ3950.z3950_2001 import *
from PyZ3950.asn1 import decode


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


