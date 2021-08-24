
import sqlite3


con = sqlite3.connect("Zoladex.db")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
# cursor.execute("DROP TABLE brand_application")
# print("Table dropped")