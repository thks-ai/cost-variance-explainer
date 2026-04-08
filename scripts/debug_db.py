from app.database.db import get_conn

def debug_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, user_final FROM reason_log")
    rows = cur.fetchall()
    conn.close()

    print("=== reason_log contents ===")
    for r in rows:
        print(r)

if __name__ == "__main__":
    debug_db()
