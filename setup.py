#!/usr/bin/env python

from distutils.core import setup

import vers

setup (name="PyZ3950",
       version= vers.version,
       author = "Aaron Lav",
       author_email = "asl2@pobox.com",
       license = "X",
       description = 'Z39.50 (ZOOM API), ASN.1, and MARC',
       long_description =
       """Pure Python implementation of ASN.1 and Z39.50 v2,
       with a simple MARC parser thrown in.  See the URL for details.""",
       platforms = "Any Python 2.1 or later",
       url = "http://www.pobox.com/~asl2/software/PyZ3950",
       packages = ["PyZ3950"])
