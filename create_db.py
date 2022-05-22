from sqlite3 import connect

connection = connect('store.sqlite')
curs = connection.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
curs.executescript(text)
curs.close()
connection.close()
