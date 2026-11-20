import sqlite3
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "dev-secret-key"

def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    conn = get_db()
    # FLAW 1: Unsanitized f-string interpolation (SQL Injection)
    query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
    user = conn.execute(query).fetchone()
    conn.close()

    if user:
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return jsonify({"status": "logged_in", "user": user["username"], "role": user["role"]})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/api/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    # FLAW 2: Fetches note by ID without checking owner_id (IDOR)
    note = conn.execute("SELECT id, title, secret_content FROM notes WHERE id = ?", (note_id,)).fetchone()
    conn.close()

    if note:
        return jsonify(dict(note))
    return jsonify({"error": "Note not found"}), 404

if __name__ == "__main__":
    app.run(port=5000)
