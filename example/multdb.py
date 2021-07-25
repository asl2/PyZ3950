from PyZ3950 import zoom

conn = zoom.Connection('www.lib.csu.ru', 210)
conn.databaseName = 'arefd+knigi+liter+period'
conn.preferredRecordSyntax = 'USMARC'
query = zoom.Query ('CCL', 'ti=Journal or au=Turgenev')
res = conn.search (query)
for r in res:
    print("db:", repr(r.databaseName), r)
