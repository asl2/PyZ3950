#!/usr/bin/env python
from PyZ3950 import zoom, z3950

zoom.trace_extract = 1
#z3950.msg_size = 0x600
conn = zoom.Connection ('z3950.loc.gov', 7090)

#conn = zoom.Connection ('ipac.lib.uchicago.edu', 210)
conn.databaseName = 'VOYAGER'
#conn.databaseName = 'uofc'
conn.preferredRecordSyntax = 'USMARC'

query = zoom.Query ('CCL', 'au=Thucydides')

res = conn.search (query)
res.presentChunk = 1
for a in res:
    print(a)

conn.close ()

