import sqlite3

DATABASE = 'products.db'

def check_user(email):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            print(f"User with email {email} exists: {user}")
        else:
            print(f"No user found with email {email}")

