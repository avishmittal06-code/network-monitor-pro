import sqlite3
from datetime import datetime

DB_NAME = "network_history.db"

def init_db():
    """Initializes the SQLite database table."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_logs (
                timestamp TEXT,
                target_name TEXT,
                host TEXT,
                type TEXT,
                latency REAL,
                status TEXT
            )
        ''')
        conn.commit()

def log_to_db(name, host, target_type, latency, status):
    """Logs a single check event to the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO performance_logs VALUES (?, ?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, host, target_type, latency, status)
        )
        conn.commit()
