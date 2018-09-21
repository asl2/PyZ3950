#!/usr/bin/env python

from PyZ3950 import zoom

def run ():
    conn = zoom.Connection ('amicus.nlc-bnc.ca', 210)
    conn.databaseName = 'NL'
    q = zoom.Query ('CCL', 'ti="1066"')
    ss = conn.scan (q)
    for s in ss[0:10]:
        print(s)
    

if __name__ == '__main__':
    run ()
