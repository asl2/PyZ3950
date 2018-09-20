This code is licensed under the X license.  It requires Dave Beazley's
PLY parsing package from http://systems.cs.uchicago.edu/ply/, licensed
under the LGPL (I've tested with both 1.0 and 1.1), and Python 2.1
(or, in all probability, later versions.)
 
For Z39.50 functionality, you probably just want to use ZOOM, in
zoom.py.  An example is in test/test1.py, which just queries the
Library of Congress for works whose title begins with "1066 and all
that".  The documentation for the language-independent API is available
at http://zoom.z3950.org/api, and I hope that should be sufficient
when combined with the docstrings in zoom.py and the example.  (If
not, please write me.)

The ASN.1 functionality is designed to be usable separately, and
lives entirely in asn1.py.  I probably should split this out into
its own package.

Aaron Lav
asl2@pobox.com





