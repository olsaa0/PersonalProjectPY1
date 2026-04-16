import sqlite3
from datetime import datetime

DB_NAME = "crypto.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            api_price REAL,
            scraped_price REAL,
            spread REAL,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_history(symbol, api_p, scrap_p, spread):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (symbol, api_price, scraped_price, spread, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (symbol, api_p, scrap_p, spread, datetime.now()))
    conn.commit()
    conn.close()
