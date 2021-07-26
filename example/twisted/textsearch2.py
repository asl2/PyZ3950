#!/usr/bin/env python



"""Like textsearch.py, but uses string.find, not regexps.  Casual
benchmarking suggests it's about the same speed as textsearch.py,
but it's easier to implement 'and not', and perhaps a little more
elegant."""

from twisted.internet import reactor, protocol

from PyZ3950 import oids

import textsearch
import ztwist

class RegExpAttribXlate (ztwist.AttribXlate):
    """Converts a Z39.50 query to a Python regexp."""
    oid = oids.Z3950_ATTRS_BIB1_ov

    def translate (self, query):
        lam = ztwist.AttribXlate.translate (self, query)
        return lam
    def term_xlate (self, aval, term):
        if aval != 1016: # USE attribute 'generic'
            self.raise_err (114, str (aval), self.eb)
        return lambda s: -1 != s.find (term)
    def combiner (self, operator, r1, r2):
        if operator == 'and':
            return lambda s: (r1 (s) and r2 (s))
        elif operator == 'or':
            return lambda s: (r1 (s) or r2 (s))
        elif operator == 'and_not':
            return lambda s: (r1(s) and not r2(s))
        else: # prox
            self.raise_err (110, operator)

class TextSearcher2(textsearch.TextSearcher):
    def check_match (self, line):
        return self.lam (line)
    def translate_query (self, query, eb):
        self.lam = RegExpAttribXlate (eb).translate (query)
        if self.lam == None:
            return 0 # eb has already been called
        return 1

class TextSearchServer2 (textsearch.TextSearchServer):
    searcher_factory = TextSearcher2

if __name__ == '__main__':
    textsearch.run (TextSearchServer2)


    





