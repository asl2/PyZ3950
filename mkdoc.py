#!/usr/bin/env python
"""Hackish code to generate online web page documentation.  At some
point I should replace this with a more standard solution."""

import hacked_pydoc as pydoc

import vers

mydir = 'PyZ3950/'

fil = open (mydir + 'index.html', "w")

def echo_file (fil,fn, repl = 0):
    f = open (fn)
    s = f.read ()
    if repl:
        s = s.replace ("$version$", str (vers.version))        
    fil.write (s)

def do_header (fil, s):
    fil.write ("<H1>" + s + "</H1>")
    
echo_file (fil, 'header', repl = 1)



mod_dict = {}

mydir = 'PyZ3950/'

def do_pydoc (fil,modname, write_link = 0):
    pydoc.writedoc (mydir + modname)
    if write_link:
        fil.write("""<p><a href="%s.html">Link to pydoc documentation for %s
        implementation (recommended interface).</a>""" % (
            modname, modname))

def do_dummy_pydoc (modname):
    hdr = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
 "http://www.w3.org/TR/html4/strict.dtd">
<html><head><title>PyZ3950 - Python Z39.50 and ASN.1 BER implementations
</title></head><body>"""
    f = open (mydir + modname + ".html", "w")
    f.write (hdr)
    f.write ('<p>Documentation is available in the <a href="./index.html">' +
             'main file</a>.')
    f.write ('</body></html>')
    f.close ()

def do_imp (modname):
    mod_dict [modname] = __import__ (mydir + modname)

do_header (fil, 'ZOOM')
mainmod = 'zoom'
do_pydoc (fil,mainmod, 1)
for mod in ['ccl', 'grs1', 'zmarc','bib1msg', 'CQLParser', 'SRWDiagnostics',
            'c2query', 'oids', 'pqf']:
    do_pydoc (fil, mod)

NamesList = ['z3950','asn1']

for n in NamesList:
    do_dummy_pydoc (n)

for n in NamesList:
    do_header (fil,n)
    do_imp (n)
    fil.write (mod_dict [n].__doc__)

echo_file (fil,'footer')





