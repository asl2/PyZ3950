#!/usr/bin/env python
from PyZ3950 import zoom

conn = zoom.Connection ('z3950.loc.gov', 7090)
conn.databaseName = 'VOYAGER'
conn.preferredRecordSyntax = 'USMARC'

query = zoom.Query ('CCL', 'ti="1066 and all that"')

res = conn.search (query)
for r in res:
    print r
conn.close ()

