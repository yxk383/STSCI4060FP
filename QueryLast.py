"""
STSCI 4060 - Final Project
Yunxi Kou - yk799
Step 7. Query the BeeGenes table for the last entry by providing GI number.
"""
import cx_Oracle

def output_type_handler(cursor, name, default_type, size, precision, scale):
    '''
    Fetch CLOB into long string
    Source: Using CLOB and BLOB Data, cx_Oracle 8.1.0 documentation
    https://cx-oracle.readthedocs.io/en/latest/user_guide/lob_data.html
    
    Modified by removing BLOB branch as it is never used.
    According to the documentation, our CLOB file is less than 1GB,
    and therefore can be printed directly.
    '''
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)


con = cx_Oracle.connect("python/py39fp")
con.outputtypehandler = output_type_handler
cur = con.cursor()

result = cur.execute("SELECT * FROM BeeGenes WHERE gi = 147907436")

print(result.fetchall())

cur.close()
con.close()