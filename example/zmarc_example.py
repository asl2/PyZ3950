#!/usr/bin/env python
"""
Use the PyZ3950 zoom & marc scripts to:
-run a Z39.50 query
-save the results to a set of files
-parse the Author from the saved results files

PyZ3950 <http://www.pobox.com/~asl2/software/PyZ3950/>
is part of Aaron Lav's Tyrannioware
<http://www.pobox.com/~asl2/software/Tyrannio/>
This example created by Andrew Ittner <http://www.rhymingpanda.com/>,
with some alterations by Aaron.
"""
import os
import tempfile

from PyZ3950 import zoom
from PyZ3950 import zmarc

def RunQuery():
    "Run a Z39.50 query & save MARC results to files"
    #open connection
    conn = zoom.Connection ('z3950.loc.gov', 7090)
    conn.databaseName = 'VOYAGER'
    conn.preferredRecordSyntax = 'USMARC'
    
    #setup query
    query = zoom.Query('CCL', 'ti="1066 and all that"')
    
    #run query
    res = conn.search(query)
    
    #for each record in the resultset, save as file
    ifilecount = 0
    for r in res:
        sSaveAs = os.path.join(tempfile.gettempdir(),
                               "PyZ3950 search resultset %d.bin" % ifilecount)
        print("Saving as file:", sSaveAs)
        fx = open(sSaveAs, "wb")
        fx.write(r.data)
        fx.close()
        ifilecount += 1
        #parse each record as we save
        ParseRecord(sSaveAs)
    #close connection
    conn.close()


def _GetValue(skey, tlist):
    """Get data for subfield code skey, given the subfields list."""
    for (subkey, subval) in tlist:
        if skey == subkey:
            return subval
    return None


def ParseRecord(sMARCfilename):
    """Given a MARC file, open & parse it
    See <http://www.loc.gov/marc/umb/> for the basics regarding the MARC
    format,
    or <http://www.loc.gov/marc/bibliographic/ecbdhome.html> for more
    details.  Unfortunately the terminology used in these two documents
    is not quite the same.
    """

    #try to open MARC file
    try:
        fz = open(sMARCfilename, "rb")
        vMARC = zmarc.MARC(fz.read())
        names_fields = [100, 700]
        #100 Main entry -- Personal name -- (primary author)
        #700 additional personal name entry
        
        for fieldno in names_fields: #show raw zmarc structure
            if fieldno not in vMARC.fields:
                continue
            
            print("Raw zmarc structure, field %d: %s" %  (
                fieldno, str(vMARC.fields[fieldno])))

            subfield_key = 'a' # text of author's name
            
            # Now, iterate over possibly multiple fields, unpacking
            # indicator 1, indicator 2, and subfields
            for (ind1, ind2, subfields) in vMARC.fields [fieldno]:
                sx = _GetValue(subfield_key, subfields)
                # Note that most of the other subfields may be
                # required to distinguish among authors, too.
                if sx != None:
                    print("Author field %d sub %s: %s" % (fieldno,
                                                          subfield_key, sx))
                else:
                    print("No $%s subfield for %d" % (subfield_key, fieldno))
    finally:
        fz.close()
    
if __name__ == '__main__':
    RunQuery()

# Parsing zMARC data:
# Our goal is to extract, from the personal author fields, either 100
# or 700, the data for subfield code 'a', which is the author name.

# vMARC.fields[X], where X is the MARC field number, will get you a list of
# field data, one element for each repetition of the field in the MARC data
# (except that 0 repetitions of field X is represented by the absence of
# key X from the "fields" dict, not a 0-length field.)

# The field data is either just the raw string (for a fixed field), or,
# for a non-fixed (XXX) field, a 3-element tuple of:
# (indicator 1, indicator 2, subdata)
# subdata is a list of tuples of (subfield code, data).
# The significance of indicators is different for each field.

# For example, here's how the Author field (100) is packed:

# list 0 (field 100 is not repeatable, so only one element in list)
#[('1', ' ', [('a', 'Arkell, Reginald,'), ('d', '1882-')])]
# tuple at 0
#('1', ' ', [('a', 'Arkell, Reginald,'), ('d', '1882-')])
# list at 2
#[('a', 'Arkell, Reginald,'), ('d', '1882-')]

# Note that the 'd' subfield (or other subfields) may be required to
# distinguish *this* Reginald Arkell from some other Reginald Arkell, but
# we ignore it for purposes of this demo, and just get the tuple with 'a'
# as its first element
#('a', 'Arkell, Reginald,')

# and now, our final goal, the second element of that tuple, which is: 

#'Arkell, Reginald,'

# the $a subfield might not be the first field, so that's why _GetValue
# runs through the tuples to find it.  Note that in general, subfields
# can be repeated, and their order wrt to the other subfields can be
# significant, which is why nothing like _GetValue is provided in zmarc.


#Note: not all records have a 100 field, and not all records have
#exactly one personal author.  I believe all records are supposed
#to have exactly one of (100,110,111,130) fields for a "main entry",

#e.g. LC control number 70953691, which has a 130 (uniform title) of
#130 0_ |a Bible. |p O.T. |l Hebrew. |f 1969.
#and 700 (author added entry) of
#700 1_ |a Fisch, Harold
#or 
#LC control number 89028075, which has a 111 (meeting author) of
#111 2_ |a National Symposium NEW CROPS: Research, Development, 
#Economics |n (1st : |d 1988 : |c Indianapolis, Ind.) 
#and 700 records of
#700 1_ |a Janick, Jules, |d 1931-
#700 1_ |a Simon, James E.
