
import sqlite3

con = sqlite3.connect("Zoladex.db")
cursor = con.cursor()

# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())
# cursor.execute("ALTER TABLE brand_products ADD datetime TEXT NOT NULL;")
# print("Column added")
cursor.execute("ALTER TABLE brand_products DROP COLUMN user_id")
print("Table dropped")