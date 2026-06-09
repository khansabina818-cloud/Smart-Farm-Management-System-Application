import sqlite3
from tkinter import messagebox

DB_NAME = "agrosmart.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    try:
        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS farmers(
            farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            village TEXT,
            land REAL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS crops(
            crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            crop_name TEXT,
            start_date DATE,
            end_date DATE
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            amount REAL,
            note TEXT,
            date DATE
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            amount REAL,
            date DATE
        )
        """)

        cur.execute("SELECT COUNT(*) FROM users")

        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                ('admin', 'admin123')
            )

        con.commit()
        con.close()

    except Exception as e:
        messagebox.showerror("DB Error", str(e))