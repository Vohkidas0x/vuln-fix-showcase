# Vulnerable Web App & Remediation Showcase (SQLi + IDOR)

A self-contained Python/Flask security engineering lab demonstrating two **OWASP Top 10** vulnerabilities, an automated Proof-of-Concept (PoC) exploit script, and the corresponding code-level remediations.

## Project Structure
    vuln-fix-showcase/
    ├── init_db.py              # Initializes SQLite database with sample users & notes
    ├── vulnerable/
    │   └── app.py              # Intentionally vulnerable Flask application
    ├── patched/
    │   └── app.py              # Hardened Flask application with security fixes
    └── exploits/
        └── poc_exploit.py      # Automated Python exploit demonstrating both flaws

## Vulnerabilities & Code Remediation

### 1. SQL Injection — Authentication Bypass (CWE-89)
* **Root Cause:** User-supplied `username` and `password` inputs were interpolated directly into a SQL query string using Python f-strings, allowing `admin' --` to comment out the password check.
* **Fix:** Replaced string interpolation with parameterized queries (`?` placeholders).

    - query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
    + query = "SELECT id, username, role FROM users WHERE username = ? AND password = ?"
    + user = conn.execute(query, (username, password)).fetchone()

### 2. Broken Object Level Authorization / IDOR (CWE-639)
* **Root Cause:** `/api/notes/<note_id>` queried records solely by `id`, allowing any authenticated user (`alice`) to read private notes belonging to `admin`.
* **Fix:** Enforced object ownership by binding the SQL `WHERE` clause to `session["user_id"]` and hardened session key generation.

    - app.secret_key = "dev-secret-key"
    + app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))

    - note = conn.execute("SELECT id, title, secret_content FROM notes WHERE id = ?", (note_id,)).fetchone()
    + note = conn.execute("SELECT id, title, secret_content FROM notes WHERE id = ? AND owner_id = ?", (note_id, session["user_id"])).fetchone()

## Setup & Reproduction

1. **Install & Initialize Database:** `python3 -m venv venv && source venv/bin/activate && pip install flask requests && python3 init_db.py`
2. **Test Vulnerable Target:** Run `python3 vulnerable/app.py &` then `python3 exploits/poc_exploit.py` (returns `200 OK` with stolen admin note).
3. **Verify Patched Target:** Run `python3 patched/app.py &` then `python3 exploits/poc_exploit.py` (blocked with `401` and `404`).

## Disclaimer
Built strictly for educational security research and defensive code-remediation practice in an isolated local environment.
