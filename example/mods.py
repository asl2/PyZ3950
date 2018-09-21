#!/usr/bin/env python

from PyZ3950 import zoom, zmarc

def make_conn ():
    conn = zoom.Connection ('z3950.loc.gov', 7090)
    conn.databaseName = 'VOYAGER'
    conn.preferredRecordSyntax = 'USMARC'
    return conn


def fetch_mods (query):
    res = conn.search (query)
    mods_list = []
    for r in res:
        marc_obj = zmarc.MARC (r.data)
        mods_list.append (marc_obj.toMODS ())
    return mods_list

conn = make_conn ()
mods_list = fetch_mods (zoom.Query ('CCL', 'ti="1066 and all that"'))
print(mods_list)


    
