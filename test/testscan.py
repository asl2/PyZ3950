#!/usr/bin/env python

from PyZ3950 import zoom

def run ():
    conn = zoom.Connection ('amicus.nlc-bnc.ca', 210)
    conn.databaseName = 'NL'

    q = zoom.Query ('CCL', 'ti=A')
    conn.numberOfEntries = 80
    ss = conn.scan (q)
    for i in range (len (ss)):
        print ss.get_term (i), ss.get_fields (i)

if __name__ == '__main__':
    run ()
