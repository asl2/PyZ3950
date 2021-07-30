#!/usr/bin/env python3

from PyZ3950.zoom import Connection, Query, SortKey


if __name__ == "__main__":
    c = Connection('gondolin.hist.liv.ac.uk', 210)
    c.databaseName = 'l5r'
    #c = Connection('z3950.copac.ac.uk', 210)
    #c.databaseName = 'COPAC'
    c.preferredRecordSyntax = 'SUTRS'
    q = Query('pqf', '@attr 1=4 "sword"')
    q2 = Query('pqf', '@attr 1=3201 foo')
    rs = c.search(q)
    print(len(rs))
    print(rs[0].data)
    sk = SortKey()

    #sk.sequence = q2

    sk.type = "private"
    sk.sequence = "/card/name"
    sk.relation = "descending"

    #sk.sequence = "rank"
    #sk.type = "elementSetName"

    rs2 = c.sort([rs], [sk])
    print(rs2[0].data)
