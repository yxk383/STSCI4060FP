"""
STSCI 4060 - Final Project
Yunxi Kou - yk799
Step 7. Query the BeeGenes table for the last entry by providing GI number.
"""
import cx_Oracle

def output_type_handler(cursor, name, default_type, size, precision, scale):
    '''
    Fetch CLOB into long string
    '''
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)

con = cx_Oracle.connect("python/py39fp")
cur = con.cursor()

result = cur.execute("SELECT * FROM BeeGenes WHERE gi = 147907436")

connection.outputtypehandler = output_type_handler

print(result.fetchall())

cur.close()
con.close()