import sqlite3

with open('seed.sql', 'r') as sql_file:
    sql_script = sql_file.read()

sqliteConnection = sqlite3.connect('groceries.db')

cursor = sqliteConnection.cursor()

cursor.executescript(sql_script)

print('DB Init')

cursor.close()

sqliteConnection.close()
