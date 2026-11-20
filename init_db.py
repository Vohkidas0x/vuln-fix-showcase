import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users")
cur.execute("DROP TABLE IF EXISTS notes")

cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    secret_content TEXT NOT NULL
)
""")

cur.executemany(
    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    [
        ("admin", "SuperS3cretAdminPass!", "admin"),
        ("alice", "alice123", "user"),
    ],
)

cur.executemany(
    "INSERT INTO notes (owner_id, title, secret_content) VALUES (?, ?, ?)",
    [
        (1, "Admin API Keys", "PROD_API_KEY=sk_live_987654321"),
        (2, "Alice's Grocery List", "Milk, Eggs, Coffee"),
    ],
)

conn.commit()
conn.close()
print("[+] Database initialized successfully.")
