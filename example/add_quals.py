#!/usr/bin/env python

"""Demonstrates adding qualifiers at runtime by mutating ccl.qual_dict,
and calling ccl.relex ()."""

from PyZ3950 import zoom, ccl

ccl.add_qual ('AUPERSONAL', (1,1))

conn = zoom.Connection ('z3950.loc.gov', 7090)
conn.databaseName = 'VOYAGER'
conn.preferredRecordSyntax = 'USMARC'

query = zoom.Query ('CCL', 'aupersonal=MacLane, Saunders')

res = conn.search (query)
for r in res[:20]:
    print(r)

conn.close ()

