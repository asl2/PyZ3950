# PyZ3950

<img src="https://travis-ci.org/danizen/PyZ3950.svg?branch=master" alt="Build Status">

## Summary

Pure-python Z39.50 implementation

## Update Notes 

This code is updated to support both Python 2.7+ and Python 3.5+ using 2to3
and some hand changes.  The one test I got working in Python 2.7 is updated
to both remain a test script and a "unit test", and that leads to test coverage
of about 40%.

However, only code in PyZ3950 is actually covered by these tests. It should 
be assumed that the code in the example, ill, and other directories
are not working properly, despite the use of 2to3. 

Updating test/test2.py indicates only that the NLM Z39.50 server does
not support concurrent searches.

As such, it is too early to release a new version, but there is enough
here to continue.   In particular, it will be good to see whether we can
utilize the asn1 library and pymarc.

Dan Davis <dan@danizen.net>

## Original README

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

Aaron Lav <asl2@pobox.com>

## License

X Consortium License (Note that since X-Windows is now covered by the MIT License, this may be soon, but I hesitate to change it without the constructive agreement of the author.)






