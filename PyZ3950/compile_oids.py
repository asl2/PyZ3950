#!/usr/bin/env python

# Original by Robert Sanderson, modifications by Aaron Lav

import sys
from PyZ3950 import asn1

inh = file("oids.txt")
outh = file("oids.py", "w")
outh.write('from PyZ3950 import asn1\n')
# from ... to get same globals as others importing asn1
outh.write('oids = {}\n')

oids = {}
vars = {}

for line in inh:
    if (not line.isspace()):
        flds = line.split(None)
        name = flds[0]
        number = flds[1]
        if (len(flds) > 2):
            aliasList = flds[2:]
        else:
            aliasList = []

        if (number[0] == "."):

            # add to previous
            splitname = name.split("_")
            cur = oids
            for n in splitname[:-1]:
                cur = cur[n]

            val = cur['val'] + [int(number[1:])]
            oid = asn1.OidVal(val)

            cur [splitname[-1]] = {'oid': oid, 'val' : val}
            
            vars[name] = val
            tree = "oids['%s']" % "']['".join (splitname)
            outh.write(tree + " = " + "{'oid': asn1.OidVal(" + str(val) + "), 'val': " + str(val) + "}\n")

        else:
            # base
            splitnums = number.split('.')
            numlist = map(int, splitnums)
            
            oids[name] = {}
            oids[name]['oid'] = asn1.OidVal(numlist)
            oids[name]['val'] = numlist
            vars[name] = numlist  

            outh.write("oids['" + name + "'] = {'oid': asn1.OidVal(" + str(numlist) + "), 'val': " + str(numlist) + "}\n")
            

inh.close()

items = vars.items()
items.sort()
for k,v in items:
    outh.write(k + " = " + str(v) + "\n")
    outh.write(k + "_ov = asn1.OidVal(" + str (v) + ")\n")

outh.close()
