import pytest

from PyZ3950 import asn1

# The code in asn1.py Tester class should be broken up into individual
# tests and moved here.  But this at least gets it run.

# asn1.py still has some python 3 string / bytes confusion in the testing code.
# Expect it to fail for now.
@pytest.mark.xfail
def test_asn1():
    tester = asn1.Tester(print_test=0)
    tester.run()
    
