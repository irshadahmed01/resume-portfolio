import sqlite3

conn = sqlite3.connect('C:/Users/notir/resume-portfolio/Practice01/day9/investments.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(investments_cleaned)")
print("Table Structure:")
print(cursor.fetchall())
conn.close()