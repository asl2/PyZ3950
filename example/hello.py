#!/usr/bin/env python
from PyZ3950 import zoom

conn = zoom.Connection ('z3950.loc.gov', 7090)
conn.databaseName = 'VOYAGER'
conn.preferredRecordSyntax = 'USMARC'

query = zoom.Query ('CCL', 'isbn=0253333490')

res = conn.search (query)
print(res [0])

conn.close ()

