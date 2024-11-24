import sqlite3


conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    type TEXT NOT NULL,
    color TEXT NOT NULL,
    photo TEXT,
    link TEXT
)
''')


conn.commit()
conn.close()

