import sqlite3

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    type TEXT,
    color TEXT,
    photo TEXT,
    link TEXT
)
''')

DATABASE = 'products.db'

create_users_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
'''

with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()
    cursor.execute(create_users_table_query)
    conn.commit()




conn.commit()
conn.close()
