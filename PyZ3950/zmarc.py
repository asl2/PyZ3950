#!/usr/bin/env python

"""Parses MARC-format data.  The MARC class has a constructor
which takes binary MARC data.
"""

# This file should be available from
# http://www.pobox.com/~asl2/software/PyZ3950/
# and is licensed under the X Consortium license:
# Copyright (c) 2001, Aaron S. Lav, asl2@pobox.com
# All rights reserved. 

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, provided that the above
# copyright notice(s) and this permission notice appear in all copies of
# the Software and that both the above copyright notice(s) and this
# permission notice appear in supporting documentation. 

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR ANY CLAIM, OR ANY SPECIAL
# INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE. 

# Except as contained in this notice, the name of a copyright holder
# shall not be used in advertising or otherwise to promote the sale, use
# or other dealings in this Software without prior written authorization
# of the copyright holder.

import sys
import string

from xml.sax.saxutils import escape

class MarcError (Exception):
    pass

def is_fixed (num):
    return num < 10

fieldsep = '\x1e'
sep = '\x1f' # XXX or 1D for pseudo-marc output from z3950.c
recsep = '\x1d'


# Attributes for SGML DTD (!!!)  If not present, then I1 I2
attrHash = { 22 : ['ISDSLvl', 'I2'], 
             24 : ['StdNum', 'DiffInd'],    28 : ['PubNmTyp', 'NteAdEnty'],
             33 : ['DateType', 'EventTyp'], 34 : ['ScapeTyp', 'I2'],
             41 : ['TransInd', 'I2'],       45 : ['TimePrd', 'I2'],
             50 : ['InLofC', 'CNSrc'],      55 : ['InNLC', 'CNCLSSrc'],
             60 : ['InNLM', 'CNSrc'],       70 : ['InNAL', 'I2'],
             72 : ['I1', 'CodeSrc'],        82 : ['Edition', 'CNSrc'],
             86 : ['NumbrSrc', 'I2'],      100 : ['NameType', 'I2'],
             110: ['NameType', 'I2'],      111 : ['NameType', 'I2'],
             130: ['NFChars', 'I2'],       150 : ['I1', 'NFChars'],
             151: ['I1', 'NFChars'],       210 : ['AddEnty', 'I2'],
             211: ['AddEnty', 'NFChars'],  212 : ['AddEnty', 'I2'],
             214: ['AddEnty', 'NFChars'],  222 : ['I1', 'NFChars'],
             240: ['PrntDisp', 'NFChars'], 242 : ['AddEnty', 'NFChars'],
             243: ['PrntDisp', 'NFChars'], 245 : ['AddEnty', 'NFChars'],
             246: ['NCAddEty', 'TitleTyp'],247 : ['AddEnty', 'NoteCntl'],
             270: ['Level', 'AddrType'],   355 : ['CntlElmt', 'I2'],
             362: ['DTFormat', 'I2'],      400 : ['NameType', 'Pronoun'],
             410: ['NameType', 'Pronoun'], 411 : ['NameType', 'Pronoun'],
             430: ['I1', 'NFChars'],       440 : ['I1', 'NFChars'],
             450: ['I1', 'NFChars'],       451 : ['I1', 'NFChars'],
             490: ['Traced', 'I2'],        505 : ['DCC', 'CDLevel'],
             510: ['CoverLoc', 'I2'],      511 : ['DCC', 'I2'],
             516: ['DCC', 'I2'],           521 : ['DCC', 'I2'],
             520: ['DCC', 'I2'],           522 : ['DCC', 'I2'],
             524: ['DCC', 'I2'],           535 : ['Holds', 'I2'],
             537: ['DCC', 'I2'],           551 : ['I1', 'NFChars'],
             555: ['DCC', 'I2'],           556 : ['DCC', 'I2'],
             565: ['DCC', 'I2'],           567 : ['DCC', 'I2'],
             581: ['DCC', 'I2'],           582 : ['DCC', 'I2'],
             586: ['DCC', 'I2'],           600 : ['NameType', 'SubjSys'],
             610: ['NameType', 'SubjSys'], 611 : ['NameType', 'SubjSys'],
             630: ['NFChars', 'SubjSys'],  650 : ['SubjLvl', 'SubjSys'],
             651: ['I1', 'SubjSys'],       653 : ['IndexLvl', 'I2'],
             654: ['IndexLvl', 'I2'],      655 : ['Type', 'Source'],
             656: ['I1', 'Source'],        656 : ['I1', 'Source'],
             700: ['NameType','EntryType'],710 : ['NameType','EntryType'],
             711: ['NameType','EntryType'],730 : ['NFChars','EntryType'],
             740: ['NFChars','EntryType'], 760 : ['NoteCntl', 'I2'],
             762: ['NoteCntl', 'I2'],      765 : ['NoteCntl', 'I2'],
             767: ['NoteCntl', 'I2'],      772 : ['NoteCntl', 'I2'],
             773: ['NoteCntl', 'I2'],      775 : ['NoteCntl', 'I2'],
             776: ['NoteCntl', 'I2'],      777 : ['NoteCntl', 'I2'],
             780: ['NoteCntl', 'RelType'], 785 : ['NoteCntl', 'RelType'],
             787: ['NoteCntl', 'I2'],      800 : ['NameType', 'I2'],
             810: ['NameType', 'I2'],      811 : ['NameType', 'I2'],
             830: ['I1', 'NFChars'],       852 : ['Scheme', 'Order'],
             853: ['CmprsExpnd', 'Eval'],  853 : ['CmprsExpnd', 'Eval'],
             856: ['AccsMeth', 'I2'],      863 : ['EncLevel', 'HoldForm'],
             864: ['EncLevel','HoldForm'], 865 : ['EncLevel', 'HoldForm'],
             866: ['EncLevel','Notation'], 867 : ['EncLevel', 'Notation'],
             868: ['EncLevel','Notation'], 886 : ['FldType', 'I2']}

subfieldHash = {'1' : "one", '2' : "two", '3' : "three", '4' : "four", '5' : "five",
                '6' : "six", '7' : "seven", '8' : "eight", '9' : "nine", '0' : "zero"}


# takes text, turns it into tuple of (ind1, ind2, list of (subfield, val))
# where subfield may repeat within the list.
# We need a structure like this in order to correctly parse both records:
# 650  0 $aWorld War, 1939-1945$xCampaigns$zTunisia
# 650  0 $aReal property$zMississippi$zTippah County$xMaps
# (taken from _USMARC Format for Bibliographic Data_, Prepared by Network
# Development and MARC Standards Office, Cataloging Distribution Service,
# Library of Congress, section 650 p. 5, page printed Dec 1991, looseleaf
# binder issued in 1988.

def parse_sub (field):
    if len (field) < 4:
        if field == '  ':
            # Is this legit?  I've seen it, so handle correctly.
            # specifically for au=Johansen, Arnold S from z3950.bibsys.no:2100
            return (' ', ' ', [])
        return None

    if field [2] <> sep:
        print "Bad field [2]", repr (field[2])
        return None
    ind1 = field[0]
    ind2 = field[1]
    sublist = []
    splitlist = string.split (field[2:], sep)
    for sub in splitlist:
        if (sub == ''): # we begin w/ sep, so there's an empty prefix
            continue
        sublist.append ((sub[0], string.strip(sub[1:])))
    return (ind1, ind2, sublist)
    
class MARC:
    """Parses data into 'fields' attribute, indexed by field number.
    Each value is a list.  For fixed fields, it's a list of the string data
    (one string for each occurence of the field in the original data).  For
    other fields, each list element is a tuple of (indicator 1, indicator 2,
    subdata), where subdata is a list of tuples of (subfield indicator,
    subfield data).  Yes, this is kinda lame and I really should have
    used structures, but this was some of the first Python code I ever
    wrote.
    """
    hdrbits = [5,6,7,8,17,18,19]
    # Status, Type, Bib. Level, Type of Ctrl., Enc. Level,
    # Descr. Cat. Form, Linked Rcd Reqt are all part of pseudoentry 0

    def __init__(self, MARC = None, strict = 1):
        """Parses MARC data.  According to Bill Oldroyd (Bill.Oldroyd at
        bl.uk), some servers don't set the character set and/or other
        bits of the MARC header properly, so it's useful to set strict=0
        when dealing with such servers."""
        self.fields = {}
        self.ok = 0
        self.marc = MARC
        if MARC == None:
            return # we'll write to it later
        reclen = self.extract_int (0,4)
        self.reclen = reclen
        baseaddr = self.extract_int (12, 16)
        zerostr = ""
        for ind in self.hdrbits: zerostr = zerostr + self.marc[ind]
        self.fields [0] = [zerostr]
        if strict:
            assert (self.marc[9] == ' ') # 'a' would be UCS/Unicode
            assert (self.marc[10] == '2' and self.marc[11] == '2')
            assert (self.marc[20:22] == '45')
        pos = 24
        lastpos = baseaddr
        while pos < baseaddr:
            tag = self.marc[pos:pos+3]
            if tag [0] == '\035' or tag [0] == '\036':
                break
            fieldlen = self.extract_int (pos + 3, pos + 6)
            startpos = self.extract_int (pos + 7, pos + 11)
            pos = pos + 12
            start = baseaddr + startpos
            end   = start + fieldlen
            line = self.marc[start:end]
            lastpos = startpos
            if line [-1] == '\x1E':
                line = line[:-1]
            else: print "Weird, no hex 1E for", tag, repr(line)
            field = string.atoi (tag)
            if is_fixed (field):
                self.fields[field] = [line]
                # 1-elt list for orthogonality of processing
            else:
                ps = parse_sub (line)
                if ps == None:
                    raise MarcError (line)
                self.fields.setdefault (field, []).append (ps)
        self.ok = 1
        # XXX should do more error-checking
    def __str__ (self):
        k = self.fields.keys ()
        k.sort ()
        lst = []
        for field in k:
            lst.append (self.stringify_field (field))
        return "MARC: \n" + "\n".join (lst)
    def stringify_field (self, k):
        f = self.fields [k]
        if is_fixed (k):
            return str (k) + " " +  f[0]
        else:
            str_l = []
            for l in f:
                def fmt (x):
                    return '$%s%s' % (x[0], x[1])
                sl = map (fmt, l[2])
                str_l.append (str(k) + " " + l[0] + l[1] + " ".join (sl))
            return "\n".join (str_l)
    def extract_int (self, start, end):
        return string.atoi (self.marc[start:end+1])
    def get_MARC (self):
        hdrlist = [' '] * 24
        zerostr = self.fields [0][0]
        for i in range (len (zerostr)):
            hdrlist [self.hdrbits [i]] = zerostr [i]
        hdrlist [10] = '2' # replace these with data map, assert on read
        hdrlist [11] = '2'
        hdrlist [20] = '4'
        hdrlist [21] = '5'
        hdrlist [22] = '0'
        hdrlist [23] = '0'
        # later - 0-4 log. record length, 12-16 base addr of data
        # directory: 3 of tag, 4 of field len, 5 of starting pos (rel.
        # to base address of data, 12-16
        fields = self.fields.keys ()
        data = ''
        directory = ''
        for field in fields:
            if field == 0: # pseudofield
                continue
            for fielddat in self.fields [field]:
                start = len (data)
                if is_fixed (field):
                    data += fielddat
                else:
                    sublist = (fielddat [0] + fielddat [1] +
                               "".join (map (lambda s: sep + s[0] + s[1],
                                             fielddat[2])))
                    data += sublist
                data += fieldsep # XXX is this right?

                length = len (data) - start
                directory += "%.03d%.04d%.05d" % (field, length, start)
        def id (x): return x
        data += fieldsep + recsep
        hdrlist [0:5] = map (id, "%.05d" % (len (hdrlist) + len (directory) +
                                   len (data),))
        hdrlist [12:17] = map (id,"%.05d" % (len (hdrlist) + len (directory),))
        return "".join (hdrlist) + directory + data

    def toMARCXML(self):
        " Convert record to MarcXML Schema "
        keys = self.fields.keys()
        keys.sort()


        xmllist = ["<record>\n", "  <leader>%s</leader>\n" % (self.get_MARC()[:24])]

        for key in keys:
            if key == 0:
                # XXX Skip?? What are these??
                pass
            elif key < 10:
                xmllist.append("  <controlfield tag=\"00%d\">%s</controlfield>\n" % (key, self.fields[key][0]))
            else:
                for instance in self.fields[key]:
                    if key < 100:
                        keystr = "0" + str(key)
                    else:
                        keystr = str(key)
                    xmllist.append("  <datafield tag=\"%s\" ind1=\"%s\" ind2=\"%s\">\n" % (keystr, instance[0], instance[1]))
                    for sub in instance[2]:
                        xmllist.append("    <subfield code=\"%s\">%s</subfield>\n" % (sub[0], escape(sub[1])))
                    xmllist.append("  </datafield>\n")

        xmllist.append("</record>")
        xml = ''.join(xmllist)
        return xml

    def toOAIMARC(self):
        """Convert record to OAI MARC XML Schema.
        Note Well that OAI-MHP 2.0 recommends using MarcXML"""
        
        keys = self.fields.keys()
        keys.sort()
        marc = self.get_MARC()

        # What should these attributes really be?
        xmllist  = ['<oai_marc type="%s" level="%s">\n' % (marc[6], marc[7])]

        for key in keys:
            if key == 0:
                # Skip?? What are these?
                pass
            elif key < 10:
                xmllist.append("  <fixfield id=\"%d\">%s</fixfield>\n" % (key, self.fields[key][0]))
            else:
                for instance in self.fields[key]:
                    xmllist.append("  <varfield tag=\"%d\" i1=\"%s\" i2=\"%s\">\n" % (key, instance[0], instance[1]))
                    for sub in instance[2]:
                        xmllist.append("    <subfield label=\"%s\">%s</subfield>\n" % (sub[0], escape(sub[1])))
                    xmllist.append("  </varfield>\n")

        xmllist.append("</oai_marc>")
        xml = ''.join(xmllist)
        return xml        

    def sgml_processCode(self, k):
        if attrHash.has_key(k):
            i1 = attrHash[k][0]
            i2 = attrHash[k][1]
        else:
            i1 = "I1"
            i2 = "I2"
        if k < 100:
            keystr = "0%d" % (k)
        else:
            keystr = str(k)

        sgmllist = []
        for instance in self.fields[k]:
            sgmllist.append('        <fld%s %s="%s" %s="%s">\n' % (keystr, i1, instance[0], i2, instance[1]))
            for sub in instance[2]:
                stag = sub[0]
                if subfieldHash.has_key(stag):
                    stag = subfieldHash[stag]
                sgmllist.append('          <%s>%s</%s>\n' % (stag, escape(sub[1]), stag))
            sgmllist.append('        </fld%s>\n' % (keystr))
        sgml = ''.join(sgmllist)
        return sgml
        

    def toSGML(self):
        """ Convert record to USMARC SGML """

        keys = self.fields.keys()
        keys.sort()

        # Extract field ranges
        cflds = []
        numbcode = []
        mainenty = []
        titles = []
        edimprnt = []
        physdesc = []
        series = []
        notes = []
        subjaccs = []
        addenty = []
        linkenty = []
        saddenty = []
        holdaltg = []
        fld9xx = []
        # Ugly
        for k in keys:
            if k == 0:
                pass
            elif k < 10:
                cflds.append(k)
            elif k < 100:
                numbcode.append(k)
            elif k < 200:
                mainenty.append(k)
            elif k < 250:
                titles.append(k)
            elif k < 300:
                edimprnt.append(k)
            elif k < 400:
                physdesc.append(k)
            elif k < 500:
                series.append(k)
            elif k < 600:
                notes.append(k)
            elif k < 700:
                subjaccs.append(k)
            elif k < 760:
                addenty.append(k)
            elif k < 800:
                linkenty.append(k)
            elif k < 840:
                saddenty.append(k)
            elif k < 900:
                holdaltg.append(k)
            else:
                fld9xx.append(k)


                 
        marc = self.get_MARC()

        sgml = ["<usmarc>\n"]
        sgml.append("  <leader>\n")
        sgml.append("    <lrl>%s</lrl>\n" % (marc[:5]))
        sgml.append("    <recstat>%s</recstat>\n" % (marc[5]))
        sgml.append("    <rectype>%s</rectype>\n" % (marc[6]))
        sgml.append("    <biblevel>%s</biblevel>\n" % (marc[7]))
        sgml.append("    <ucp>%s</ucp>\n" % (marc[8:10]))
        sgml.append("    <indcount>%s</indcount>\n" % (marc[10]))
        sgml.append("    <sfcount>%s</sfcount>\n" % (marc[11]))
        sgml.append("    <baseaddr>%s</baseaddr>\n" % (marc[12:17]))
        sgml.append("    <enclevel>%s</enclevel>\n" % (marc[17]))
        sgml.append("    <dsccatfm>%s</dsccatfm>\n" % (marc[18]))
        sgml.append("    <linkrec>%s</linkrec>\n" % (marc[19]))
        sgml.append("    <entrymap>\n")
        sgml.append("      <flength>%s</flength>\n" % (marc[20]))
        sgml.append("      <scharpos>%s</scharpos>\n" % (marc[21]))
        sgml.append("      <idlength>%s</idlength>\n" % (marc[22]))
        sgml.append("      <emucp>%s</emucp>\n" % (marc[23]))
        sgml.append("    </entrymap>\n")
        sgml.append("  </leader>\n")
        sgml.append("  <directry></directry>\n")

        sgml.append("  <varflds>\n")
        sgml.append("    <varcflds>\n")
        for k in cflds:
            sgml.append("      <fld00%d>%s</fld00%s>\n" % (k, self.fields[k][0], k))
        sgml.append("    </varcflds>\n")
        sgml.append("    <vardflds>\n")
        sgml.append("      <numbcode>\n")
        for k in numbcode:
            sgml.append(self.sgml_processCode(k))
        sgml.append("      </numbcode>\n")

        if mainenty:
            sgml.append("      <mainenty>\n")
            for k in mainenty:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </mainenty>\n")
        if titles:
            sgml.append("      <titles>\n")
            for k in titles:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </titles>\n")
        if edimprnt:
            sgml.append("      <edimprnt>\n")
            for k in edimprnt:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </edimprnt>\n")
        if physdesc:
            sgml.append("      <physdesc>\n")
            for k in physdesc:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </physdesc>\n")
        if series:
            sgml.append("      <series>\n")
            for k in series:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </series>\n")
        if notes:
            sgml.append("      <notes>\n")
            for k in notes:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </notes>\n")
        if subjaccs:
            sgml.append("      <subjaccs>\n")
            for k in subjaccs:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </subjaccs>\n")
        if addenty:
            sgml.append("      <addenty>\n")
            for k in addenty:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </addenty>\n")
        if linkenty:
            sgml.append("      <linkenty>\n")
            for k in linkenty:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </linkenty>\n")
        if saddenty:
            sgml.append("      <saddenty>\n")
            for k in saddenty:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </saddenty>\n")
        if holdaltg:
            sgml.append("      <holdaltg>\n")
            for k in holdaltg:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </holdaltg>\n")
        if fld9xx:
            sgml.append("      <fld9xx>\n")
            for k in fld9xx:
                sgml.append(self.sgml_processCode(k))
            sgml.append("      </fld9xx>\n")
        sgml.append("    </vardflds>\n")
        sgml.append("  </varflds>\n")
        sgml.append("</usmarc>")
        return ''.join(sgml)
        

    def toSimpleDC(self):
        """ Convert Marc into DC according to LC Crosswalk """
        xml = ['<dc xmlns="http://www.loc.gov/zing/srw/dcschema/v1.0/">\n']

        # Title -> 245
        if self.fields.has_key(245):
            instance = self.fields[245][0][2]
            a = ''
            b = ''
            for sub in instance:
                if sub[0] == 'a':
                    a = sub[1]
                elif sub[0] == 'b':
                    b = sub[1]
            if a and b and a[-1] in [',', '.', ';', ':']:
                a += " " + b
            elif a and b:
                a += "; " + b
            elif b and not a:
                a = b
            xml.append("  <title>%s</title>\n" % (a))

        # Creator -> 100,110,111,700,710,711
        authorKeys = [100, 110, 111, 700, 710, 711]
        for k in authorKeys:
            if self.fields.has_key(k):
                for instance in self.fields[k]:
                    a = ''
                    h = ''
                    d = ''
                    for sub in instance[2]:
                        if sub[0] == 'a':
                            a = sub[1]
                        elif sub[0] == 'h':
                            h = sub[1]
                        elif sub[0] == 'd':
                            d = sub[1]
                    if h:
                        a += ", " + h
                    if d:
                        a += " (" + d + ")"
                    xml.append("  <creator>%s</creator>\n" % (a))
        
        # Subject -> 600,610, 611, 630, 650, 653
        # Just dump in directly...
        subjectList = [600, 610, 611, 630, 650, 653]
        for s in subjectList:
            if self.fields.has_key(s):
                for instance in self.fields[s]:
                    subject = ''
                    for sub in instance[2]:
                        subject += sub[1] + " -- "
                    subject = subject[:-4]
                    xml.append("  <subject>%s</subject>\n" % (subject))
        

        # Publisher -> 260$a$b
        if self.fields.has_key(260):
            for instance in self.fields[260]:
                a = b = ''
                for sub in instance[2]:
                    if sub[0] == 'a':
                        a = sub[1]
                    elif sub[0] == 'b':
                        b = sub[1]
                        if b[-1] in [',', ';', ':']:
                            b = b[:-1]
                    elif sub[0] == 'c':
                        d = sub[1]
                        if d[-1] == '.':
                            d = d[:-1]
                        xml.append("  <date>%s</date>\n" % (d))
                if b:
                    a += " " + b
                if a:
                    xml.append("  <publisher>%s</publisher>\n" % (a))

        # Type -> 655
        if self.fields.has_key(655):
            for instance in self.fields[655]:
                gf = ''
                for sub in instance[2]:
                    gf  += sub[1] + " -- "
                gf = gf[:-4]
                xml.append("  <type>%s</type>\n" % (gf))

        # Non Standard:  Identifier -> ISSN/ISBN
        for k in [20,22]:
            if self.fields.has_key(k):
                for instance in self.fields[k]:
                    for sub in instance[2]:
                        if sub[0] == 'a':
                            xml.append("  <identifier>%s</identifier>\n" % (sub[1]))

        # Non Standard: Description -> 300
        if self.fields.has_key(300):
            for instance in self.fields[300]:
                desc = ''
                for sub in instance[2]:
                    desc += sub[1] + " "
                desc = desc[:-1]
                xml.append("  <description>%s</description>\n" % (desc))
                
        xml.append("</dc>")
        return ''.join(xml)


    def toMODS(self):
        """ Tranform MARC record into MODS according to CrossWalk """
        xml = ["<mods>\n"]

        # --- TitleInfo Fields ---
        if self.fields.has_key(245):
            instance = self.fields[245][0][2]
            xml.append("  <titleInfo>\n    <title>")
            insubtitle = 0
            for sub in instance:
                if (sub[0] in ['a', 'f', 'g', 'k']):
                    xml.append(escape(sub[1]))
                    xml.append(' ')
                elif (sub[0] == 'b'):
                    xml.append("</title>\n    <subtitle>%s " % (escape(sub[1])))
                    insubtitle = 1
            if (insubtitle):
                xml.append("</subtitle>\n  </titleInfo>\n")
            else:
                xml.append("</title>\n  </titleInfo>\n")

        if self.fields.has_key(210):
            instance = self.fields[210][0][2]
            subf = {}
            for sub in instance:
                subf[sub[0]] = escape(sub[1])
            xml.append('  <titleInfo type="abbreviated">\n    <title>%s</title>\n' % (subf['a']))
            if (subf.has_key('b')):
                xml.append('    <subtitle>%s</subtitle>\n' % (subf['b']))
            xml.append('  </titleInfo>\n')

        if self.fields.has_key(242):
            instance = self.fields[242][0][2]
            subf = {}
            for sub in instance:
                subf[sub[0]] = escape(sub[1])
            if (subf.has_key('i')):
                label = ' displayLabel="%s"' % (subf['i'])
            else:
                label = ''
            xml.append('  <titleInfo type="translated"%s>\n    <title>%s</title>\n' % (label, subf['a']))
            if (subf.has_key('b')):
                xml.append('    <subtitle>%s</subtitle>\n' % (subf['b']))
            if (subf.has_key('n')):
                xml.append('    <partNumber>%s</partNumber>\n' % (subf['n']))
            if (subf.has_key('p')):
                xml.append('    <partName>%s</partName>\n' % (subf['p']))
            xml.append('  </titleInfo>\n')
                

        if self.fields.has_key(246):
            full = self.fields[246][0]
            subfield2 = full[1]
            instance = full[2]
            subf = {}
            for sub in instance:
                subf[sub[0]] = escape(sub[1])
            if (subfield2 == 1):
                xml.append('  <titleInfo type="translated">\n    <title>%s</title>\n' % (subf['a']))
            else:
                xml.append('  <titleInfo type="alternative">\n    <title>%s</title>\n' % (subf['a']))

            if (subf.has_key('b')):
                xml.append('    <subtitle>%s</subtitle>\n' % (subf['b']))
            if (subf.has_key('n')):
                xml.append('    <partNumber>%s</partNumber>\n' % (subf['n']))
            if (subf.has_key('p')):
                xml.append('    <partName>%s</partName>\n' % (subf['p']))
            xml.append('  </titleInfo>\n')

        if self.fields.has_key(130):
            uniform = self.fields[130][0][2]
        elif self.fields.has_key(240):
            uniform = self.fields[240][0][2]
        else:
            uniform = []
        if (uniform):
            subf = {}
            for sub in uniform:
                subf[sub[0]] = escape(sub[1])
            xml.append('  <titleInfo type="uniform">\n    <title>%s</title>\n' % (subf['a']))
            if (subf.has_key('n')):
                xml.append('    <partNumber>%s</partNumber>\n' % (subf['n']))
            if (subf.has_key('p')):
                xml.append('    <partName>%s</partName>\n' % (subf['p']))
            xml.append('  </titleInfo>\n')


        # --- Name Fields ---
        # Creator -> 100,110,111, 700,710,711
        authorKeyTypes = {100 : 'personal',  110 : 'corporate', 111 : 'conference', 700 : 'personal', 710 : 'corporate',  711 : 'conference'}

        for k in authorKeyTypes.keys():
            if self.fields.has_key(k):
                for instance in self.fields[k]:
                    subf = {}
                    for sub in instance[2]:
                        subf[sub[0]] = escape(sub[1])
                    xml.append('  <!-- Marc: %s -->\n' % (k))
                    xml.append('  <name type="%s">\n' % (authorKeyTypes[k]))
                    xml.append('    <role><roleTerm type="text">creator</roleTerm></role>\n')
                    xml.append('    <namePart>%s</namePart>\n' % (subf['a']))
                    if (subf.has_key('d')):
                        xml.append('    <namePart type="date">%s</namePart>\n' % (subf['d']))
                    if (subf.has_key('b')):
                        if (k in [100,700]):
                            xml.append('    <namePart type="termsOfAddress">%s</namePart>\n' % (subf['b']))
                        else:
                            xml.append('    <namePart>%s</namePart>\n' % (subf['b']))
                    if (subf.has_key('e')):
                        xml.append('    <role><roleTerm type="text">%s</roleTerm></role>\n' % (subf['e']))
                    if (subf.has_key('4')):
                        xml.append('    <role><roleTerm type="code">%s</roleTerm></role>\n' % (subf['4']))
                    xml.append('  </name>\n')

        ldr = self.fields[0][0]
        type = ldr[1]
        types = {'a' : 'text', 't' : 'text', 'e' : 'cartographic', 'f' : 'cartographic', 'c' : 'notated music', 'd' : 'notated music', 'i' : 'sound recording - nonmusical', 'j' : 'sound recording - musical', 'k' : 'still image', 'g' : 'moving image', 'r' : 'three dimensional object', 'm' : 'software, multimedia', 'p' : 'mixed material'}
        if (types.has_key(type)):
            xml.append('  <typeOfResource')
            if (ldr[2] == 'c'):
                xml.append(' collection="yes"')
            if (ldr[1] in ['d', 'f', 'p', 't']):
                xml.append(' manuscript="yes"')
            xml.append('>%s</typeOfResource>\n' % (types[type]))


        if (self.fields.has_key(8)):
            instance = self.fields[8][0]
            # XXX LONG set of checks for type and various 008 positions :(
            if (len(instance) > 33 and instance[33] == '0'):
                xml.append('  <genre authority="marcgt">non fiction</genre>\n')
                
        if self.fields.has_key(655):
            for instance in self.fields[655]:
                gf = ''
                for sub in instance[2]:
                    gf  += escape(sub[1]) + " -- "
                gf = gf[:-4]
                xml.append("  <genre>%s</genre>\n" % (gf))

        # PublicationInfo from 260
        f260 = self.fields.get(260, [])
        f44 = self.fields.get(44, [])
        f46 = self.fields.get(46, [])
        f250 = self.fields.get(250, [])
        f310 = self.fields.get(310, [])
        f321 = self.fields.get(321, [])
        f8 = self.fields.get(8, [])

        if f260 or f46 or f250 or f310 or f321:
            xml.append('  <originInfo>\n')

            if (f8 and len(f8[0]) > 18 ):
                loc = f8[0][15:18]
                if (loc <> '   ' and loc <> '|||'): 
                    xml.append('    <place><placeTerm type="code" authority="marccountry">%s</placeTerm></place>\n' % (loc))

            if (f44):
                for s in f44[0][2]:
                    if (s[0] == 'c'):
                        xml.append('    <place><placeTerm type="code" authority="iso3166">%s</placeTerm></place>\n' % (escape(s[1])))
            if (f260):
                instance = self.fields[260][0][2]            
                subf260 = {}
                for sub in instance:
                    subf260[sub[0]] = escape(sub[1])
                if (subf260.has_key('a')):
                    xml.append('    <place><placeTerm type="text">%s</placeTerm></place>\n' % (subf260['a']))
                if (subf260.has_key('b')):
                    xml.append('    <publisher>%s</publisher>\n' % (subf260['b']))
                if (subf260.has_key('c')):
                    xml.append('    <dateIssued>%s</dateIssued>\n' % (subf260['c']))

            if (f8 and len(f8[0]) > 6):
                f8type = f8[0][6]
                if (f8type in ['e', 'p', 'r', 's', 't']):
                    date = f8[0][7:11]
                    if (date <> '    '):
                        xml.append('    <dateIssued encoding="marc">%s</dateIssued>\n' % (date))
                if (f8type in ['c', 'd', 'i', 'k', 'm', 'u', 'q']):
                    if (f8type == 'q'):
                        attrib = ' qualifier="questionable"'
                    else:
                        attrib = ""
                    start = f8[0][7:11]
                    if (start <> '    '):
                        xml.append('    <dateIssued point="start" encoding="marc"%s>%s</dateIssued>\n' % (attrib, start))
                    end = f8[0][11:15]
                    if (end <> '    '):
                        xml.append('    <dateIssued point="end" encoding="marc"%s>%s</dateIssued>\n' % (attrib, end))

            if (f260):
                if subf260.has_key('g'):
                    xml.append('    <dateCreated>%s</dateCreated>\n' % (escape(subf260['g'])))

            if (f46):
                instance = f46[0][2]
                subf46 = {}
                for s in instance:
                    subf46[s[0]] = escape(s[1])
                if (subf46.has_key('k')):
                    xml.append('    <dateCreated point="start">%s</dateCreated>\n' % (subf46['k']))
                if (subf46.has_key('l')):
                    xml.append('    <dateCreated point="end">%s</dateCreated>\n' % (subf46['l']))
                if (subf46.has_key('m')):
                    xml.append('    <dateValid point="start">%s</dateValid>\n' % (subf46['m']))
                if (subf46.has_key('n')):
                    xml.append('    <dateValid point="end">%s</dateValid>\n' % (subf46['n']))
                if (subf46.has_key('j')):
                    xml.append('    <dateModified>%s</dateModified>\n' % (subf46['j']))

            if (f250):
                for s in f250[0][2]:
                    if (s[0] == 'a'):
                        xml.append('    <edition>%s</edition>\n' % (escape(s[1])))
                        break
            
            if (self.fields.has_key(0) and len(self.fields[0][0]) > 2):
                f0type = self.fields[0][0][2]
                if (f0type in ['b', 'i', 's']):
                    xml.append('    <issuance>continuing</issuance>\n')
                elif (f0type in ['a', 'c', 'd', 'm']):
                    xml.append('    <issuance>monographic</issuance>\n')

            if (f310):
                subf310 = {'a' : '', 'b' : ''}
                for s in f310[0][2]:
                    subf310[s[0]] = escape(s[1])
                xml.append('    <frequency>%s %s</frequency>\n' % (subf310['a'], subf310['b']))
            if (f321):
                subf321 = {'a' : '', 'b' : ''}
                for s in f321[0][2]:
                    subf321[s[0]] = escape(s[1])
                xml.append('    <frequency>%s %s</frequency>\n' % (subf321['a'], subf321['b']))
            xml.append('  </originInfo>\n')
                

        # --- Language ---
        if (f8 and len(f8[0]) > 38):
            lang = f8[0][35:38]
            if (lang <> '   '):
                xml.append('  <language><languageTerm type="code" authority="iso639-2b">%s</languageTerm></language>\n' % (lang))
        if self.fields.has_key(41):
            a = two = ''
            for sub in self.fields[41][0][2]:
                if sub[0] == 'a':
                    a = sub[1]
                elif sub[0] == '2':
                    two = sub[1]
                elif sub[0] == 'd' and not a:
                    a = sub[1]
                elif sub[0] == 'e' and not a:
                    a = sub[1]

            if a and not two:
                xml.append('  <language><languageTerm authority="iso639-2b">%s</languageTerm></language>\n' % (escape(a)))
            elif a:
                xml.append('  <language authority="%s">%s</language>\n' % (escape(two), escape(a)))

        # --- Physical Description ---
        # XXX: Better field 008, 242,245,246$h, 256$a
        f300 = self.fields.get(300, [])
        if (f8 and len(f8[0]) > 23):
            f8_23 = self.fields[8][0][23]
        else:
            f8_23 = ' '
        if (f300 or f8_23 == ' '):
            xml.append("  <physicalDescription>\n")
            if (f8_23 == ' '):
                xml.append('    <form authority="marcform">print</form>\n')
            if f300:
                desclist = []
                for s in f300[0][2]:
                    desclist.append(escape(s[1]))
                desc = ' '.join(desclist)
                xml.append("    <extent>%s</extent>\n" % (desc))
            xml.append("  </physicalDescription>\n")

        # Abstract
        if self.fields.has_key(520):
            xml.append('  <abstract>')
            for sub in self.fields[520]:
                if sub[0] == 'a' or sub[0] == 'b':
                    xml.append(escape(sub[1]))
            xml.append("</abstract>\n")

        # --- Table of Contents ---
        if (self.fields.has_key(505)):
            desclist = []
            for s in self.fields[505][0][2]:
                if (s[0] in ['a', 'g', 'r', 't']):
                    desclist.append(escape(s[1]))
            toc = ' '.join(desclist)
            xml.append('  <tableOfContents>%s</tableOfContents>\n' % (toc))

        # XXX TargetAudience (field 8 again)

        # --- Note ---
        if (self.fields.has_key(500)):
            for n in (self.fields[500]):
                xml.append('  <note>');
                for s in n:
                    if (s[0] == 'a'):
                        xml.append(escape(s[1]))
                xml.append('</note>\n')

        # --- Subject ---
        subjectList = [600, 610, 611, 630, 650, 651, 653]
        for s in subjectList:
            if self.fields.has_key(s):
                for instance in self.fields[s]:
                    xml.append("  <subject")
                    auths = {'0' : 'lcsh',
                             '1' : 'lcshac',
                             '2' : 'mesh',
                             '3' : 'csh',
                             '5' : 'nal',
                             '6' : 'rvm'}
                    if (auths.has_key(instance[1])):
                        xml.append(' authority="%s"' % auths[instance[1]])
                    xml.append(">\n")

                    if (s in [600, 610, 611]):
                        stype = {600 : 'personal', 610 : 'corporate', 611 : 'conference'}[s]
                        xml.append('    <name type="%s">\n' % (stype))
                        for sub in instance[2]:
                            val = escape(sub[1])
                            if (sub[0] == 'a'):
                                xml.append('      <namePart>%s</namePart>\n' % (val))
                            elif (sub[0] == 'b'):
                                attrib = ''
                                if (s == 600):
                                    attrib = ' type="termsOfAddress"'
                                xml.append('      <namePart%s>%s</namePart>\n' % (attrib, val))
                            elif (sub[0] == 'd'):
                                xml.append('      <namePart type="date">%s</namePart>\n' % (val))
                            elif (sub[0] == 'e'):
                                xml.append('      <role><roleTerm type="text">%s</roleTerm></role>\n' % (val))
                            elif (sub[0] == '4'):
                                xml.append('      <role><roleTerm type="code">%s</roleTerm></role>\n' % (val))
                            elif (sub[0] == 'u'):
                                xml.append('      <affiliation>%s</affiliation>\n' % (val))
                            elif sub[0] in ['v', 'x']:
                                xml.append('      <topic>%s</topic>\n' % (val))
                            elif sub[0] == 'y':
                                xml.append('      <temporal>%s</temporal>\n' % (val))
                            elif sub[0] == 'z':
                                xml.append('      <geographic>%s</geographic>\n' % (val))
                        xml.append('    </name>\n')
                    elif (s == 630):
                        for sub in instance[2]:
                            val = escape(sub[1])
                            if (sub[0] == 'a'):
                                xml.append('    <title>%s</title>\n' % (val))
                            elif (sub[0] == 'p'):
                                xml.append('    <partName>%s</partName>\n' % (val))
                            elif (sub[0] == 'n'):
                                xml.append('    <partNumber>%s</partNumber>\n' % (val))
                            elif sub[0] in ['v', 'x']:
                                xml.append('    <topic>%s</topic>\n' % (val))
                            elif sub[0] == 'y':
                                xml.append('    <temporal>%s</temporal>\n' % (val))
                            elif sub[0] == 'z':
                                xml.append('    <geographic>%s</geographic>\n' % (val))
                    elif (s in [650, 653]):
                        for sub in instance[2]:
                            val = escape(sub[1])
                            if (sub[0] == 'a'):
                                xml.append('    <topic>%s</topic>\n' % (val))
                            elif sub[0] in ['v', 'x']:
                                xml.append('    <topic>%s</topic>\n' % (val))
                            elif sub[0] == 'y':
                                xml.append('    <temporal>%s</temporal>\n' % (val))
                            elif sub[0] == 'z':
                                xml.append('    <geographic>%s</geographic>\n' % (val))
                    elif (s == 651):
                        for sub in instance[2]:
                            val = escape(sub[1])
                            if (sub[0] == 'a'):
                                xml.append('    <geographic>%s</geographic>\n' % (val))
                            elif sub[0] in ['v', 'x']:
                                xml.append('    <topic>%s</topic>\n' % (val))
                            elif sub[0] == 'y':
                                xml.append('    <temporal>%s</temporal>\n' % (val))
                            elif sub[0] == 'z':
                                xml.append('    <geographic>%s</geographic>\n' % (val))
                                
                    xml.append("  </subject>\n")
        if (self.fields.has_key(45)):
            full = self.fields[45][0]
            if (full[0] in ['0', '1']):
                for x in self.fields[2]:
                    if (x[0] == 'b'):
                        xml.append('  <subject><temporal encoding="iso8601">%s</temporal></subject>\n' % (escape(x[1])))
                        
        if (self.fields.has_key(43)):
            for sub in self.fields[43][0][2]:
                if (sub[0] == 'a'):
                    xml.append('  <subject><geographicCode authority="marcgac">%s</geographicCode></subject>\n' % (escape(sub[1])))
                elif (sub[0] == 'a'):
                    xml.append('  <subject><geographicCode authority="iso3166">%s</geographicCode></subject>\n' % (escape(sub[1])))

        if (self.fields.has_key(752)):
            xml.append('  <subject><hierarchicalGeographic>\n')
            for sub in self.fields[43][0][2]:
                val = escape(sub[1])
                if (sub[0] == 'a'):
                    xml.append('    <country>%s</country>\n' % (val))
                elif (sub[0] == 'b'):
                    xml.append('    <state>%s</state>\n' % (val))
                elif (sub[0] == 'c'):
                    xml.append('    <county>%s</county>\n' % (val))
                elif (sub[0] == 'd'):
                    xml.append('    <city>%s</city>\n' % (val))
            xml.append('  </hierarchicalGeographic></subject>')
            

        if (self.fields.has_key(255)):
            subf = {}
            xml.append('  <subject><cartographics>\n')
            for s in self.fields[255][0][2]:
                subf[s[0]] = escape(s[1])
            if (subf.has_key('c')):
                xml.append('    <coordinates>%s</coordinates>\n' % (subf['c']))
            if (subf.has_key('a')):
                xml.append('    <scale>%s</scale>\n' % (subf['a']))
            if (subf.has_key('b')):
                xml.append('    <projection>%s</projection>\n' % (subf['c']))
            xml.append('  </cartographics></subject>\n')

        if (self.fields.has_key(656)):
            for s in self.fields[656][0][2]:
                if (s[0] == 'a'):
                    xml.append('  <subject><occupation>%s</occupation></subject>\n')

        # XXX:  34

        # XXX:  Classification, 84

        cfields = {50 : 'lcc', 82 : 'ddc', 80 : 'udc', 60 : 'nlm'}
        for k in cfields:
            if (self.fields.has_key(k)):
                for sub in self.fields[k][0][2]:
                    stuff = []
                    if (sub[0] == 'a'):
                        stuff.append(escape(sub[1]))
                    elif (sub[0] == 'b'):
                        stuff.append(escape(sub[1]))
                txt = ' '.join(stuff)
                xml.append('  <classification authority="%s">%s</classification>\n' % (cfields[k], txt))

        if (self.fields.has_key(86)):
            full = self.fields[86][0]
            ind1 = full[0]
            if (ind1 == '0'):
                auth = 'sudocs'
            elif (ind1 == '1'):
                auth = 'candocs'
            else:
                auth = ''
            if (auth):
                for s in full[2]:
                    if (s[0] == 'a'):
                        xml.append('  <classification authority="%s">%s</classification>\n' % (auth, escape(s[1])))
                
                    
        # XXX:  relatedItem, 7XX

        # --- Identifier ---
        if self.fields.has_key(20):
            for instance in self.fields[20]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml.append('  <identifier type="isbn">%s</identifier>\n' % (escape(sub[1])))
        if self.fields.has_key(22):
            for instance in self.fields[22]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml.append('  <identifier type="issn">%s</identifier>\n' % (escape(sub[1])))
        if self.fields.has_key(24):
            for instance in self.fields[24]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml.append('  <identifier type="isrc">%s</identifier>\n' % (escape(sub[1])))
        if self.fields.has_key(28):
            for instance in self.fields[28]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml.append('  <identifier type="matrix number">%s</identifier>\n' % (escape(sub[1])))

        # XXX: location, accessCondition

        # --- recordInformation ---
        xml.append('  <recordInformation>\n')
        if (self.fields.has_key(40)):
            for instance in self.fields[40]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml.append('    <recordContentSource authority="marcorg">%s</recordContentSource>\n' % (escape(sub[1])))
        if (self.fields.has_key(8)):
            date = self.fields[8][0][0:6]
            if (date <> '      '):
                xml.append('    <recordCreationDate encoding="marc">%s</recordCreationDate>\n' % (date))

        if (self.fields.has_key(1)):
            xml.append('    <recordIdentifier>%s</recordIdentifier>\n' % (self.fields[1][0]))
        if (self.fields.has_key(40)):
            instance = self.fields[40][0][2]
            for s in instance:
                if (s[0] == 'b'):
                    xml.append('    <languageOfCataloging><languageTerm authority="iso639-2b">%s</languageTerm></languageOfCataloging>\n' % (escape(s[1])))

        xml.append('  </recordInformation>\n')
        xml.append("</mods>")
        txt = ''.join(xml)
        return txt

from PyZ3950 import marc_to_unicode

# see http://www.loc.gov/marc/specifications/speccharmarc8.html

import unicodedata

class MARC8_to_Unicode:
    """Converts MARC-8 to Unicode.  Note that currently, unicode strings
    aren't normalized, and some codecs (e.g. iso8859-1) will fail on
    such strings.  When I can require python 2.3, this will go away.

    Warning: MARC-8 EACC (East Asian characters) makes some
    distinctions which aren't captured in Unicode.  The LC tables give
    the option of mapping such characters either to a Unicode private
    use area, or a substitute character which (usually) gives the
    sense.  I've picked the second, so this means that the MARC data
    should be treated as primary and the Unicode data used for display
    purposes only.  (If you know of either of fonts designed for use
    with LC's private-use Unicode assignments, or of attempts to
    standardize Unicode characters to allow round-trips from EACC,
    or if you need the private-use Unicode character translations,
    please inform me, asl2@pobox.com."""


    
    basic_latin = 0x42
    ansel = 0x45
    def __init__ (self, G0 = basic_latin, G1 = ansel):
        self.g0 = G0
        self.g1 = G1

    def is_multibyte (self, charset):
        return charset == 0x31
        
    def translate (self, s):
        uni_list = []
        combinings = []
        pos = 0
        while pos < len (s):
            if s[pos] == '\x1b':
                if (s[pos +1] == s[pos+2] and
                    (s[pos +1] == '$' or s[pos+1] == '(')):
                    self.g0 = ord (s[pos+3])
                    pos = pos + 4
                    continue
            mb_flag = self.is_multibyte (self.g0)
                
            if mb_flag:
                d = (ord (s[pos]) * 65536 +
                     ord (s[pos+1]) * 256 +
                     ord (s[pos+2]))
                pos += 3
            else:
                d = ord (s[pos])
                pos += 1
                
            if (d < 0x20 or
                (d > 0x80 and d < 0xa0)):
                uni = unichr (d)
                continue
            
            if d > 0x80 and not mb_flag:
                (uni, cflag) = marc_to_unicode.codesets [self.g1] [d]
            else:
                (uni, cflag) = marc_to_unicode.codesets [self.g0] [d]
                
            if cflag:
                combinings.append (unichr (uni))
            else:
                uni_list.append (unichr (uni))
                if len (combinings) > 0:
                    uni_list += combinings
                    combinings = []
        # what to do if combining chars left over?
        uni_str = u"".join (uni_list)
        
        # unicodedata.normalize not available until Python 2.3        
        if hasattr (unicodedata, 'normalize'):
            uni_str = unicodedata.normalize ('NFC', uni_str)
            
        return uni_str

def test_convert (s, enc):
    conv = MARC8_to_Unicode ()
    converted = conv.translate (s)
    converted = unicodedata.normalize ('NFC', converted)
    print converted.encode (enc)

    print repr (converted)

        

if __name__ == '__main__':
    # My console is usually set to iso-8859-1.  Sorry if yours is different.
    test_convert('''The  oldest cuisine in the world : cooking in
    Mesopotamia  / Jean Bott\xe2ero ; translated by Teresa Lavender Fagan.''',
                 'iso-8859-1')
    
    test_convert (
        """$6 245-02/$1$a \x1b$$1!M>!`o!#!KPa!\\O!#!\x1b((B/$c \x1b$$1!1?!R_!#!-bb!#!!Gm!>`!#!\x1b((B; \x1b$$1!RY!YF!#!9Z6!#!!J(!Yi!#!\x1b((B;\x1b$$1!#!!BX!O>!#!!4`!4)!#!!\\e!#!!Hk!:M!#!\x1b((B... [et al.] ; \x1b$$1!Iq!MH!#!!9%!];!#!!KG!#!\x1b((B= Great garnishes / author, Huang Su-Huei ; translator, Yen-Jen Lai ; collaborators, Cheng-Tzu Chiu ... [et al.] ; photographers, Aki Ohno.""",
        'utf-8')
    

    for f in sys.argv[1:]:
        marc_file = open(f, 'rb')
        marc_text = marc_file.read ()
        while 1:
            marc_data1 = MARC(marc_text)
            print str (marc_data1)
            new = marc_data1.get_MARC ()
            marc_data2 = MARC (marc_text)
            k1 = marc_data1.fields.keys ()
            k2 = marc_data2.fields.keys ()
            assert (k1 == k2)
            for field in k1:
                same = (marc_data1.fields [field] ==
                        marc_data2.fields [field])
                assert (same)
            marc_text = marc_text[marc_data1.reclen:]
            if len (marc_text) == 0:
                break
        marc_file.close ()


