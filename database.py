import sqlite3
from pathlib import Path

DB_PATH = Path("guinpro.db")

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS picks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        event TEXT, selection TEXT, odds REAL, sport TEXT,
        status TEXT DEFAULT 'pending', stake REAL DEFAULT 1
    )""")
    conn.commit()
    return conn

def save_picks(items):
    with connect() as conn:
        for item in items:
            conn.execute(
                "INSERT INTO picks(event, selection, odds, sport) VALUES(?,?,?,?)",
                (item["event"], item["selection"], item["odds"], item["sport"])
            )

def summary():
    with connect() as conn:
        total, won, lost, pending = conn.execute("""
            SELECT COUNT(*),
            SUM(status='won'), SUM(status='lost'), SUM(status='pending')
            FROM picks
        """).fetchone()
    return total or 0, won or 0, lost or 0, pending or 0
