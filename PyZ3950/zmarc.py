#!/usr/bin/env python

"""Parses MARC-format data.  The MARC class has a constructor
which takes binary MARC data.
"""

# This file should be available from
# http://www.pobox.com/~asl2/software/PyZ3950/
# and is licensed under the X Consortium license:
# Copyright (c) 2001, Aaron S. Lav, asl2@pobox.com
# XML code contributed by Robert Sanderson
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


# XXX:  Python strings are immutable.  Rewrite XML translations to use
# ''.join(list_of_strings) for performance, or, even better, use
# xml.dom.minidom to construct, and then writexml ()

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

    def __init__(self, MARC = None):
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

        xml = "<record>\n"
        xml += "  <leader>%s</leader>\n" % (self.get_MARC()[:24])

        for key in keys:
            if key == 0:
                # XXX Skip?? What are these??
                pass
            elif key < 10:
                xml += "  <controlfield tag=\"00%d\">%s</controlfield>\n" % (key, self.fields[key][0])
            else:
                for instance in self.fields[key]:
                    if key < 100:
                        keystr = "0" + str(key)
                    else:
                        keystr = str(key)
                    xml += "  <datafield tag=\"%s\" ind1=\"%s\" ind2=\"%s\">\n" % (keystr, instance[0], instance[1])
                    for sub in instance[2]:
                        xml += "    <subfield code=\"%s\">%s</subfield>\n" % (sub[0], escape(sub[1]))
                    xml += "  </datafield>\n"

        xml += "</record>"
        return xml

    def toOAIMARC(self):
        """Convert record to OAI MARC XML Schema.
        Note Well that OAI-MHP 2.0 recommends using MarcXML"""
        
        keys = self.fields.keys()
        keys.sort()
        marc = self.get_MARC()

        # What should these attributes really be?
        xml = '<oai_marc type="%s" level="%s">\n' % (marc[6], marc[7])

        for key in keys:
            if key == 0:
                # Skip?? What are these?
                pass
            elif key < 10:
                xml += "  <fixfield id=\"%d\">%s</fixfield>\n" % (key, self.fields[key][0])
            else:
                for instance in self.fields[key]:
                    xml += "  <varfield tag=\"%d\" i1=\"%s\" i2=\"%s\">\n" % (key, instance[0], instance[1])
                    for sub in instance[2]:
                        xml += "    <subfield label=\"%s\">%s</subfield>\n" % (sub[0], escape(sub[1]))
                    xml += "  </varfield>\n"

        xml += "</oai_marc>"
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

        sgml = ""
        for instance in self.fields[k]:
            sgml += '        <fld%s %s="%s" %s="%s">\n' % (keystr, i1, instance[0], i2, instance[1])
            for sub in instance[2]:
                stag = sub[0]
                if subfieldHash.has_key(stag):
                    stag = subfieldHash[stag]
                sgml += '          <%s>%s</%s>\n' % (stag, escape(sub[1]), stag)
            sgml += '        </fld%s>\n' % (keystr)
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
        sgml = "<usmarc>\n"
        sgml += "  <leader>\n"
        sgml += "    <lrl>%s</lrl>\n" % (marc[:5])
        sgml += "    <recstat>%s</recstat>\n" % (marc[5])
        sgml += "    <rectype>%s</rectype>\n" % (marc[6])
        sgml += "    <biblevel>%s</biblevel>\n" % (marc[7])
        sgml += "    <ucp>%s</ucp>\n" % (marc[8:10])
        sgml += "    <indcount>%s</indcount>\n" % (marc[10])
        sgml += "    <sfcount>%s</sfcount>\n" % (marc[11])
        sgml += "    <baseaddr>%s</baseaddr>\n" % (marc[12:17])
        sgml += "    <enclevel>%s</enclevel>\n" % (marc[17])
        sgml += "    <dsccatfm>%s</dsccatfm>\n" % (marc[18])
        sgml += "    <linkrec>%s</linkrec>\n" % (marc[19])
        sgml += "    <entrymap>\n"
        sgml += "      <flength>%s</flength>\n" % (marc[20])
        sgml += "      <scharpos>%s</scharpos>\n" % (marc[21])
        sgml += "      <idlength>%s</idlength>\n" % (marc[22])
        sgml += "      <emucp>%s</emucp>\n" % (marc[23])
        sgml += "    </entrymap>\n"
        sgml += "  </leader>\n"
        sgml += "  <directry></directry>\n"

        sgml += "  <varflds>\n"
        sgml += "    <varcflds>\n"
        for k in cflds:
            sgml += "      <fld00%d>%s</fld00%s>\n" % (k, self.fields[k][0], k)
        sgml += "    </varcflds>\n"
        sgml += "    <vardflds>\n"
        sgml += "      <numbcode>\n"
        for k in numbcode:
            sgml += self.sgml_processCode(k)
        sgml += "      </numbcode>\n"

        if mainenty:
            sgml += "      <mainenty>\n"
            for k in mainenty:
                sgml += self.sgml_processCode(k)
            sgml += "      </mainenty>\n"
        if titles:
            sgml += "      <titles>\n"
            for k in titles:
                sgml += self.sgml_processCode(k)
            sgml += "      </titles>\n"
        if edimprnt:
            sgml += "      <edimprnt>\n"
            for k in edimprnt:
                sgml += self.sgml_processCode(k)
            sgml += "      </edimprnt>\n"
        if physdesc:
            sgml += "      <physdesc>\n"
            for k in physdesc:
                sgml += self.sgml_processCode(k)
            sgml += "      </physdesc>\n"
        if series:
            sgml += "      <series>\n"
            for k in series:
                sgml += self.sgml_processCode(k)
            sgml += "      </series>\n"
        if notes:
            sgml += "      <notes>\n"
            for k in notes:
                sgml += self.sgml_processCode(k)
            sgml += "      </notes>\n"
        if subjaccs:
            sgml += "      <subjaccs>\n"
            for k in subjaccs:
                sgml += self.sgml_processCode(k)
            sgml += "      </subjaccs>\n"
        if addenty:
            sgml += "      <addenty>\n"
            for k in addenty:
                sgml += self.sgml_processCode(k)
            sgml += "      </addenty>\n"
        if linkenty:
            sgml += "      <linkenty>\n"
            for k in linkenty:
                sgml += self.sgml_processCode(k)
            sgml += "      </linkenty>\n"
        if saddenty:
            sgml += "      <saddenty>\n"
            for k in saddenty:
                sgml += self.sgml_processCode(k)
            sgml += "      </saddenty>\n"
        if holdaltg:
            sgml += "      <holdaltg>\n"
            for k in holdaltg:
                sgml += self.sgml_processCode(k)
            sgml += "      </holdaltg>\n"
        if fld9xx:
            sgml += "      <fld9xx>\n"
            for k in fld9xx:
                sgml += self.sgml_processCode(k)
            sgml += "      </fld9xx>\n"
        sgml += "    </vardflds>\n"
        sgml += "  </varflds>\n"
        sgml += "</usmarc>"
        return sgml
        

    def toSimpleDC(self):
        """ Convert Marc into DC according to LC Crosswalk """
        xml = '<dc xmlns="http://purl.org/dc/elements/1.1">\n'

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
            xml += "  <title>%s</title>\n" % (a)

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
                    xml  += "  <creator>%s</creator>\n" % (a)
        
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
                    xml += "  <subject>%s</subject>\n" % (subject)
        

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
                        xml += "  <date>%s</date>\n" % (d)
                if b:
                    a += " " + b
                if a:
                    xml += "  <publisher>%s</publisher>\n" % (a)

        # Type -> 655
        if self.fields.has_key(655):
            for instance in self.fields[655]:
                gf = ''
                for sub in instance[2]:
                    gf  += sub[1] + " -- "
                gf = gf[:-4]
                xml += "  <type>%s</type>\n" % (gf)

        # Non Standard:  Identifier -> ISSN/ISBN
        for k in [20,22]:
            if self.fields.has_key(k):
                for instance in self.fields[k]:
                    for sub in instance[2]:
                        if sub[0] == 'a':
                            xml += "  <identifier>%s</identifier>\n" % (sub[1])

        # Non Standard: Description -> 300
        if self.fields.has_key(300):
            for instance in self.fields[300]:
                desc = ''
                for sub in instance[2]:
                    desc += sub[1] + " "
                desc = desc[:-1]
                xml += "  <description>%s</description>\n" % (desc)
                
        xml += "</dc>"
        return xml

    def toMODS(self):
        """ Tranform MARC record into MODS according to CrossWalk """
        xml = "<mods>\n"

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
            xml += "  <titleInfo>\n    <title>%s</title>\n  </titleInfo>\n" % (a)

        # Creator -> 100,110,111, 700,710,711
        authorKeyTypes = {100 : 'personal',  110 : 'corporate', 111 : 'conference', 700 : 'personal', 710 : 'corporate',  711 : 'conference'}

        for k in authorKeyTypes.keys():
            if self.fields.has_key(k):
                for instance in self.fields[k]:
                    name = '  <name type="%s">\n' % (authorKeyTypes[k])
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
                    name += '    <namePart>%s</namePart>\n' % (a)
                    if d:
                        name += '    <namePart type="date">%s</namePart>\n' % (d)
                    name += "    <role>creator</role>\n  </name>\n"
                    xml += name

        # XXX typeOfResource is Leader/06 or 07 
        # genre is 008/various plus ...

        if self.fields.has_key(655):
            for instance in self.fields[655]:
                gf = ''
                for sub in instance[2]:
                    gf  += sub[1] + " -- "
                gf = gf[:-4]
                xml += "  <genre>%s</genre>\n" % (gf)

        # PublicationInfo from 260
        if self.fields.has_key(260):
            pub  = '  <publicationInfo>\n'
            for sub in self.fields[260][0][2]:
                if sub[0] == 'a':
                    pub += '    <place>%s</place>' % (sub[1])
                elif sub[0] == 'b':
                    b = sub[1]
                    if b[-1] in [',', ';', ':']:
                        b = b[:-1]
                    pub += '    <publisher>%s</publisher>' % (b)
                elif sub[0] == 'c':
                    d = sub[1]
                    if d[-1] == '.':
                        d = d[:-1]
                    pub += "    <dateIssued>%s</dateIssued>\n" % (d)
                elif sub[0] == 'g':
                    d = sub[1]
                    if d[-1] == '.':
                        d = d[:-1]
                    pub += "    <dateCreated>%s</dateCreated>\n" % (d)
            if self.fields.has_key(250):
                for sub in self.fields[250][0][2]:
                    if sub[0] == 'a':
                        pub += '    <edition>%s</edition>\n' % (sub[0])
                
            pub += "  </publicationInfo>\n"
            xml += pub

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
                xml += '  <language authority="iso639-2b">%s</language>\n' % (a)
            elif a:
                xml += '  <language authority="%s">%s</language>\n' % (two, a)

        # physdesc
        # Parsing of 007 and 008
        if self.fields.has_key(300):
            xml += "  <physicalDescription>\n"
            for instance in self.fields[300]:
                desc = ''
                for sub in instance[2]:
                    desc += sub[1] + " "
                desc = desc[:-1]
                xml += "    <extent>%s</extent>\n" % (desc)            
            xml += "  </physicalDescription>\n"

        # Abstract
        if self.fields.has_key(520):
            xml += '  <abstract>\n'
            for sub in self.fields[520]:
                if sub[0] == 'a' or sub[0] == 'b':
                    xml += sub[1]
            xml += "  </abstract>\n"

        subjectList = [600, 610, 611, 630, 650, 653]
        for s in subjectList:
            if self.fields.has_key(s):
                for instance in self.fields[s]:
                    xml += "  <subject>\n"
                    for sub in instance[2]:
                        if sub[0] in ['a', 'b', 'c', 'd']:
                            xml += "    <topic>%s</topic>\n" % (sub[1])
                        elif sub[0] == 'z':
                            xml += '    <geographic>%s</geographic>\n' % (sub[1])
                        elif sub[0] == 'y':
                            xml += '    <temporal>%s</temporal>\n' % (sub[1])
                    xml += "  </subject>\n"
        
        if self.fields.has_key(20):
            for instance in self.fields[20]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml += '  <identifier type="isbn">%s</identifier>\n' % (sub[1])
        if self.fields.has_key(22):
            for instance in self.fields[22]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml += '  <identifier type="issn">%s</identifier>\n' % (sub[1])
        if self.fields.has_key(24):
            for instance in self.fields[24]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml += '  <identifier type="isrc">%s</identifier>\n' % (sub[1])
        if self.fields.has_key(28):
            for instance in self.fields[28]:
                for sub in instance[2]:
                    if sub[0] == 'a':
                        xml += '  <identifier type="matrix number">%s</identifier>\n' % (sub[1])


        xml += "</mods>"
        return xml


        

        

if __name__ == '__main__':
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


