import pandas as pd
import sqlite3 
df=pd.read_excel('intern.xlsx')
conn=sqlite3.connect('test.db')
c=conn.cursor()
#c.execute('CREATE TABLE flask1(id INTEGER NOT NULL,name TEXT NOT NULL,dept TEXT NOT NULL)')
#conn.commit()
df.to_sql('flask1',conn,if_exists='replace',index=False)
c.execute("update flask1 set name='Vyshnavi' where id='101'")
c.execute("select * from flask1")
for row in c.fetchall():
    print(row)
