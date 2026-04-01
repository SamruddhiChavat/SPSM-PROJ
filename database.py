import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, mfa_secret TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS scan_history 
            (id INTEGER PRIMARY KEY, username TEXT, filename TEXT, result TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')