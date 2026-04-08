# app/database/crud.py

from app.database.db import get_conn

def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    # variance
    cur.execute("""
    CREATE TABLE IF NOT EXISTS variance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        period TEXT NOT NULL,
        item_code TEXT NOT NULL,
        item_name TEXT,
        department TEXT,
        actual_cost REAL NOT NULL,
        standard_cost REAL NOT NULL,
        quantity REAL NOT NULL,
        variance_amount REAL NOT NULL,
        variance_type TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # reason_log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reason_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variance_id INTEGER NOT NULL,
        ai_generated TEXT NOT NULL,
        user_final TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (variance_id) REFERENCES variance(id)
    );
    """)

    # embedding_store
    cur.execute("""
    CREATE TABLE IF NOT EXISTS embedding_store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reason_log_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        vector_path TEXT NOT NULL,
        item_code TEXT,
        department TEXT,
        variance_type TEXT,
        variance_amount REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reason_log_id) REFERENCES reason_log(id)
    );
    """)

    conn.commit()
    conn.close()
