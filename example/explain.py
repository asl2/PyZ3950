#!/usr/bin/env python
from PyZ3950 import zoom

def oid_to_str (attr): # XXX for V3 this should be OID instead of str form
    return ".".join (map (str, attr.lst))
    
class Explainer:
    def __init__ (self, conn):
        self.conn = conn
        self.categories = {}
        self.databases  = {}
        self.attributes = {}
        self.record_syntaxes = []
        
    def run_query (self, qstr):
        query = zoom.Query ('CCL',qstr)
        res = conn.search (query)
        print(qstr)
        self.disp_res (res)
        return res
    def run (self):
        ret = self.run_query ('attrset (exp1/(1,1)=CategoryList)')
        assert len (ret) == 1
        (typ, cat) = ret[0].data
        assert typ == 'categoryList'
        for c in cat.categories:
            self.categories [c.category.lower()] = 1
        for info in ['targetinfo', 'databaseinfo', 'attributesetinfo',
                     'attributedetails', 'recordsyntaxinfo',
                     'sortdetails',
                     'termlistinfo', 'termlistdetails',
                     'schemainfo', 'tagsetinfo',
                     'extendedservicesinfo',
                     'elementsetdetails', 'retrievalrecorddetails',
                     'processinginfo', 'variantsetinfo', 'unitinfo']:
            if info in self.categories:
                def report_unsupp ():
                    print("client does not support", info)
                fn = getattr (self, 'run_' + info, lambda: report_unsupp ())
                print(" *** %s *** " % info)
                fn ()

            else:
                print("server does not support", info)

    def run_sortdetails (self):
        for db in list(self.databases.keys ()):
            self.run_query ('attrset(exp1/(1,1)="SortDetails" and (1,3) = %s)' % db)
    def run_recordsyntaxinfo (self):
        for rs in self.record_syntaxes:
            rs_str = oid_to_str (rs)
            self.run_query ('attrset(exp1/(1,1)="RecordSyntaxInfo" and (1,6) = %s)' % rs_str)
        

    def run_attributedetails (self):
        for db in list(self.databases.keys ()):
            self.run_query ('attrset(exp1/(1,1)="AttributeDetails" and (1,3) = %s)' % db)

    def run_attributesetinfo (self):
        for attr in list(self.attributes.keys ()):
            attr_str = oid_to_str (attr)

            self.run_query ('attrset(exp1/(1,1)="AttributeSetInfo" and (1,5) = %s)' % attr_str)

    def run_databaseinfo (self):
        for db in list(self.databases.keys ()):
            ret = self.run_query ('attrset(exp1/(1,1)="DatabaseInfo" and (1,3) = %s)' % db)

    def run_targetinfo (self):
        ret = self.run_query ('attrset (exp1/(1,1)=TargetInfo)')
        (typ, ti) = ret[0].data
        assert typ == 'targetInfo'
        if hasattr (ti, 'commonAccessInfo'):
            if hasattr (ti.commonAccessInfo, 'attributeSetIds'):
                for attr in ti.commonAccessInfo.attributeSetIds:
                    self.attributes [attr] = 1
        if hasattr (ti, 'dbCombinations'):
            dbcomb = ti.dbCombinations
            for db1 in dbcomb:
                for db2 in db1:
                    self.databases [db2] = 1
        if hasattr (ti, 'recordSyntaxes'):
            self.record_syntaxes = ti.recordSyntaxes
        
    def disp_res (self, res):
        for r in res:
            print(r)
                           

if __name__ == '__main__':
    # XXX what record syntax does catalogue.bized.ac.uk:2105 want?
    #conn = zoom.Connection ('z3950.copac.ac.uk', 210)
    # conn = zoom.Connection ('www.cnshb.ru', 210)
    #    conn = zoom.Connection ('blpcz.bl.uk', 21021)
    #     conn = zoom.Connection('sherlock.berkeley.edu', 2100)
    conn = zoom.Connection('gondolin.hist.liv.ac.uk', 210)    
    
    conn.databaseName = 'IR-Explain-1'
    conn.preferredRecordSyntax = 'EXPLAIN'
    #    conn._cli.test = 1
    e = Explainer (conn)
    e.databases['l5r'] = 1
    e.databases['scifi'] = 1
    e.run ()
    conn.close ()

