#!/usr/bin/env python

"""A demo of the ztwist Z39.50/Twisted interface.  It implements
a single database named 'TEXT', which only implements AND/OR queries for
BIB-1 use attribute 'ANY', (type=1, val=1016), searches all files
ending in .txt or .html in the current directory, and always returns
SUTRS records (with the element set name prepended)."""

import os
import sys
import re


from twisted.internet import reactor, protocol
from PyZ3950 import zdefs, asn1, zoom, oids

import ztwist

dbname = 'TEXT'

callLater = 1
# set to 1 for testing purposes, to verify code still works when
# called as part of a Twisted callback instead of from the original
# caller's context.  It doesn't seem to make much throughput difference
# (checked w/ test.py from this directory), but it adds latency.

class RegExpAttribXlate (ztwist.AttribXlate):
    """Converts a Z39.50 query to a Python regexp."""
    oid = oids.Z3950_ATTRS_BIB1_ov

    def translate (self, query):
        regexp = ztwist.AttribXlate.translate (self, query)
#        print "regexp", regexp
        if regexp == None:
            return None
        return re.compile (regexp)
    
    def term_xlate (self, aval, term):
        if aval != 1016: # USE attribute 'generic'
            self.raise_err (114, str (aval), self.eb)
        return "(%s)" % (term,)
    def combiner (self, operator, r1, r2):
        if operator == 'and':
            return "((%s.*%s)|(%s.*%s))" % (r1, r2, r2, r1) # ugh
        elif operator == 'or':
            return "(%s|%s)" % (r1, r2)
        else: # and-not, prox
            self.raise_err (110, operator)

class ResultElt:
    def __init__ (self, fn, lineno, line):
        self.fn = fn
        self.lineno = lineno
        self.line = line
    def __str__ (self):
        return '%s:%d %s' % (self.fn, self.lineno, self.line)

class TextSearcher(ztwist.ErrRaiser):
    def search (*args, **kw):
        """Calls cb with a list of record ids, or eb with an exception"""
        if callLater:
            reactor.callLater (0.01, TextSearcher.real_search, *args, **kw)
        else:
            TextSearcher.real_search (*args, **kw)
    def check_match (self, line):
        return None != self.re_comp.search (line)
    def translate_query (self, query, eb):
        self.re_comp = RegExpAttribXlate (eb).translate (query)
        if self.re_comp == None:
            return 0 # eb has already been called
        return 1
    
    def real_search (self, query, cb, eb):
        if not self.translate_query (query, eb):
            return 
        res_set = []
        for fn in os.listdir ("."):
            if not fn.endswith ('.txt') and not fn.endswith ('.html'):
                continue
            f = open(fn)
            for lineno, line in enumerate(f.readlines()):
                if self.check_match (line):
                    res_set.append (ResultElt (fn, lineno, line))
            f.close ()
            
        # need to include self in res_set so that Present can call back
        # format_one on the proper object (result sets can include multiple
        # databases)
        
        cb ([(self, r) for r in res_set])
            
    def format_one (self, rec, esn, syntax, next):
        elt_external = asn1.EXTERNAL ()
        elt_external.direct_reference = zdefs.Z3950_RECSYN_SUTRS_ov
        elt_external.encoding = ('single-ASN1-type', str(esn) + ': ' + str (rec))
        n = zdefs.NamePlusRecord ()
        n.name = dbname
        n.record = ('retrievalRecord', elt_external)
        # we could call next(n) directly, but using reactor.callLater
        # helps to ensure there aren't any bugs which would be revealed
        # by running from callback context, and prevents stack overflow
        # for large Present requests.  Normally, I'd expect some kind of
        # async call to be required to fetch the data, so 'next' should
        # be triggered from a deferred callback.  (An errback should
        # correspond to a surrogate diagnostic.)
        if callLater:
            reactor.callLater (0.01, next, n)
        else:
            next (n)

class TextSearchServer (ztwist.Z3950Server):
    searcher_factory = TextSearcher
    def __init__ (self, *args, **kw):
        self.searcher = {}
        self.searcher[dbname] = self.searcher_factory ()
        # deliberately skip ztwist.Z3950Server.__init__

def run (server):
    factory = protocol.Factory ()
    factory.protocol = server
    reactor.listenTCP (2100, factory)
    reactor.run ()


if __name__ == '__main__':
    run (TextSearchServer)
    
