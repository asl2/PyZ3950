#!/usr/bin/env python
"""Quick total hack to transform the LC-maintained webpage with
bib-1 error definitions into a Python dictionary.  Needs a tiny bit
of by-hand postprocessing.  File ends up in bib1msg.py, which is
part of the distribution, so you shouldn't ever need to run this.
"""
from __future__ import print_function

import formatter
import sys
try:
    from html.parser import HTMLParser
except ImportError:
    from htmllib import HTMLParser


class MyParser(HTMLParser):
    def __init__ (self, form):
        HTMLParser.__init__ (self, form)
        self.strlst = []
        self.lst = []
    def flush (self):
        if len (self.lst) == 0:
            return
        if len (self.lst) == 4 and self.lst [-1] == '\xa0': # nonbreaking space at end for a couple
            self.lst = self.lst [:-1]
        if len (self.lst) ==  3:
            self.strlst.append ("%s: '%s', # %s" % (self.lst [0], self.lst[1], self.lst[2]))
        else:
            print("# Bad len lst:", str (self.lst))
        self.lst = []
    def start_tr (self, attrs):
        self.flush () # needed
    def end_tr (self):
        self.flush ()
    def start_td (self, attrs):
        self.save_bgn ()
    def end_td (self):
        self.lst.append (self.save_end ())

if __name__ == '__main__':
    fil = open (sys.argv [1])
    form = formatter.NullFormatter ()
    p = MyParser (form)
    p.feed (fil.read ())
    p.close ()
    print("bib1_msg_dict = {")
    print(",\n".join (p.strlst))
    print("}")
