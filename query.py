import sqlite3
conn=sqlite3.connect('database.db')
cmd=conn.cursor()
cmd.execute('''
select * from users;
''')
print(cmd.fetchall())
conn.commit()
conn.close()