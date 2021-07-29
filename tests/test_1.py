#!/usr/bin/env python
from __future__ import print_function, absolute_import
from PyZ3950 import zoom
from io import StringIO


def get_results():
    conn = zoom.Connection ('z3950.loc.gov', 7090)
    conn.databaseName = 'VOYAGER'
    conn.preferredRecordSyntax = 'USMARC'

    query = zoom.Query ('CCL', 'ti="1066 and all that"')

    res = conn.search (query)
    for r in res:
        yield(r)
    conn.close ()


def test_1():
    results = list(get_results())
    assert len(results) == 13

    


def main():
    for r in get_results():
        print(r)


if __name__ == '__main__':
    main()
