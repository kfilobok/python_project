import sqlite3
import pytest


def test_table_structure():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()

    expected_columns = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "name", "TEXT", 1, None, 0),
        (2, "price", "REAL", 1, None, 0),
        (3, "type", "TEXT", 0, None, 0),
        (4, "color", "TEXT", 0, None, 0),
        (5, "photo", "TEXT", 0, None, 0),
        (6, "link", "TEXT", 0, None, 0)
    ]

    assert columns == expected_columns


def test_insert_and_query_by_name():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    test_data = {
        "name": "Test Product",
        "price": 100000000000,
        "type": "",
        "color": "may",
        "photo": "mylinktophoto",
        "link": "mylink"
    }


    cursor.execute("""
    INSERT INTO products (name, price, type, color, photo, link) 
    VALUES (:name, :price, :type, :color, :photo, :link)
    """, test_data)
    conn.commit()

    cursor.execute("SELECT * FROM products WHERE name = ?", (test_data["name"],))
    fetched_record = cursor.fetchone()

    assert fetched_record is not None, "Не удалось записать(((("
    assert fetched_record[1] == test_data["name"]
    assert fetched_record[2] == test_data["price"]
    assert fetched_record[3] == test_data["type"]
    assert fetched_record[4] == test_data["color"]
    assert fetched_record[5] == test_data["photo"]
    assert fetched_record[6] == test_data["link"]

    assert fetched_record[0] > 0



def test_delete_old_record():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    test_data = {
        "name": "Test Product",
        "price": 100000000000,
        "type": "",
        "color": "may",
        "photo": "mylinktophoto",
        "link": "mylink"
    }

    cursor.execute("""
    INSERT INTO products (name, price, type, color, photo, link) 
    VALUES (:name, :price, :type, :color, :photo, :link)
    """, test_data)

    conn.commit()
    cursor.execute("SELECT * FROM products WHERE name = ?", (test_data["name"],))
    fetched_record = cursor.fetchone()
    assert fetched_record is not None

    cursor.execute("DELETE FROM products WHERE name = ?", (test_data["name"],))
    conn.commit()

    cursor.execute("SELECT * FROM products WHERE name = ?", (test_data["name"],))
    deleted_record = cursor.fetchone()
    assert deleted_record is None