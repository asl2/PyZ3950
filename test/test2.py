#!/usr/bin/env python
from __future__ import print_function, absolute_import

from PyZ3950 import zoom
conn = zoom.Connection ('ilsz3950.nlm.nih.gov', 7090)
conn.databaseName = 'voyager'

conn.preferredRecordSyntax = 'MARC8'

query1 = zoom.Query ('CCL', 'au=Gould, Stephen Jay')
res1 = conn.search (query1)
query2 = zoom.Query ('CCL', 'au=Pynchon, Thomas')
res2 = conn.search (query2)
for i in range (0, max (len (res1), len (res2))):
    if i < len (res1):
        print("1:", res1[i])
    if i < len (res2):
        print("2:", res2[i])
conn.close ()

