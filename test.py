import sqlite3


sqliteConnection = sqlite3.connect('prices.db')
cursor = sqliteConnection.cursor()
print("Connected to SQLite")

sqlite_select_query = """SELECT * from target_list"""
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
print("Total rows are:  ", len(records))
for row in records:
 print(row[0])
 print("\n")

cursor.close()

