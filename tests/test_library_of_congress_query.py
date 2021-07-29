#!/usr/bin/env python
from __future__ import print_function, absolute_import
from PyZ3950 import zoom


def test_library_of_congress_query():
    conn = zoom.Connection ('z3950.loc.gov', 7090)
    conn.databaseName = 'VOYAGER'
    conn.preferredRecordSyntax = 'USMARC'

    query = zoom.Query ('CCL', 'ti="1066 and all that"')

    res = conn.search (query)
    # ensure we got at least one record
    assert len(res) >= 1
    conn.close ()
