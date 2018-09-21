#!/usr/bin/env python
from __future__ import print_function

from distutils.core import setup

import vers
import os
import os.path

# Because PLY compiles the yacc grammar to Python code, we need to run
# that compilation at install time to avoid dropping the created files
# in some random directory.  (Note that PLY's staleness checking
# depends on the MD5 hash of the repr() of assorted objects, and the
# repr is subject to change between Python versions (maybe)).

# I can't find a consistent way to import modules at build time,
# so I've removed this code for now.  (Changing directories into
# PyZ3950 works under Python 2.2 but not 2.3, importing with pathnames
# works under Linux but not Win 98 or XP.)


# We define a custom build_ext

from distutils.util import byte_compile
from distutils.command.build_ext import build_ext
from distutils.extension import Extension

pyz_dir = "PyZ3950"

class PLYBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            nm =  self.get_ext_fullname (ext.sources[0])
#            print("running %s to generate parsing tables" % (nm,))
#
#            mod = __import__ (os.path.join (pyz_dir,nm))



foo = Extension ("parsetab", ["ccl"])

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Programming Language :: Python
Topic :: Internet :: Z39.50"""

setup (name="PyZ3950",
       version= vers.version,
       author = "Aaron Lav",
       author_email = "asl2@pobox.com",
       license = "X",
       description = 'Z39.50 (ZOOM API), ASN.1, and MARC implementations',
       long_description =
       """Pure Python implementation of ASN.1 and Z39.50 v3,
       with a simple MARC parser thrown in.  See the URL for details.""",
       platforms = ["any"],
       classifiers = filter(None, classifiers.split("\n")),
       url = "http://www.pobox.com/~asl2/software/PyZ3950",
       packages = ["PyZ3950"],
       cmdclass = {'build_ext' : PLYBuild},
       ext_modules= [foo])

