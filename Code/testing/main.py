import sqlite3


con = sqlite3.connect("database.db")
cur = con.cursor()

con.execute("""CREATE TABLE IF NOT EXISTS TABLENAME(
EXAMPLENAME STRING
    
    
    )""")

cur.execute("INSERT INTO TABLENAME Values('EXAMPLE')")

con.commit()
cur.execute("SELECT * FROM TABLENAME")
print(cur.fetchall())
con.close()