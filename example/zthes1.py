#!/usr/bin/env python

"""Quick hack to retrieve Zthes GRS-1 or XML data"""

from PyZ3950 import zoom
import xml.dom.minidom as minidom

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def strip (str):
    return str.replace ('\n', '')

# XXX these types are not exhaustive!

top_types = {'PT' : 'Preferred term',
             'ND' : 'Non-preferred term',
             'NL' : 'Node label / guide term',
             'TT' : 'Top term (obsolete)'}

rel_types = {'NT': 'Narrower term',
         'BT': 'Broader term',
         'USE': 'Use instead',
         'UF': 'Use for',
         'RT': 'Related term',
         'LE': 'Linguistic equivalent'}

class Node:
    def __init__ (self, **kw):
        self.__dict__.update (kw)
    def __str__ (self):
        return " ".join (map (str, list(self.__dict__.items ())))
        
def xmlparse (s):
    print(s)
    raise Exception("XML not currently implemented")
    # see below for why this isn't implemented

def find_node (nodelist, tag):
    for n in nodelist:
        if n.tag == tag:
            return n
    return None
        
def grs1parse (g):
    # extract (2,1), (4,2) for preferred term, type.  Then map to
    # list of beneath (2,30) : (2,1),(4,3)
    # (2,1) - term name
    # (4,2) - term type
    # (2,30) - relation
    # (4,3)  - relationType
    children = g.children
    term = find_node (children, (2,1)).leaf.content[1]
    typ  = find_node (children, (4,2)).leaf.content[1]
    lst = []
    for r in children:
        if r.tag == (2,30):
            reltyp = find_node (r.children, (4,3)).leaf.content [1]
            relval = find_node (r.children, (2,1)).leaf.content [1]
            lst.append (Node (typ=reltyp, name=relval))
    return [(Node (typ = typ, name = term), lst)]



class Zthes:
    def __init__ (self, host, port, db):
        self.conn = zoom.Connection (host, port)
        self.conn.databaseName = db
        self.conn.elementSetName = 'F'
#        self.conn.preferredRecordSyntax = 'XML'
# currently (2002-7-17) the dbiref.kub.nl seems broken for XML
# in two ways:
# 1) Much more data is returned for elementSetName 'B' than 'F'.
# 2) even for 'B', the term name for the top-level record isn't
#    returned, but the term id is.  The term name isn't marked as
#    optional in the spec.
        self.conn.preferredRecordSyntax = 'GRS-1'

    def lookup (self, term):
        text = 'attrset(XD1/(1,1)="%s")' % (term,)
        q = zoom.Query ('CCL', text)
        res = self.conn.search (q)
        l = []
        parsedict = {
            'XML'   : xmlparse,
            'GRS-1' : grs1parse
            }
        for r in res:
            parser = parsedict.get (r.syntax, None)
            if parser == None:
                print(("Unknown syntax:", r.syntax, "for", r.data))
                continue

            l += parser (r.data)
        return l
        
def run ():
    zth = Zthes ('dbiref.kub.nl', 1800, 'jel')
    while 1:
        term = eval(input ('Query: '))
        if not term:
            break
        l1 =  zth.lookup (term)
        for (n, l2) in l1:
            print(("Term", n.typ, n.name))
            for e in l2:
                print(("  ", e.typ, e.name))
            print("---")
            
if __name__ == '__main__':
    run ()
