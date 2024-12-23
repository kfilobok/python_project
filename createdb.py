import sqlite3

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS LIME (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    type TEXT,
    color TEXT,
    photo TEXT,
    link TEXT,
     UNIQUE(link)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS AWN (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    type TEXT,
    color TEXT,
    photo TEXT,
    link TEXT,
    UNIQUE(link)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ZRN (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    type TEXT,
    color TEXT,
    photo TEXT,
    link TEXT,
    UNIQUE(link)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
''')

conn.commit()
conn.close()
