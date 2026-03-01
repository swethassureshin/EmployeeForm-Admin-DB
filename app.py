from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def get_db():
    conn = sqlite3.connect("employees.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/init-db")
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            emp_id TEXT,
            department TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()
    return "Database initialized"

# ---------- API ----------
@app.route("/submit", methods=["POST"])
def submit_form():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO employees (name, emp_id, department, date) VALUES (?, ?, ?, ?)",
        (data["name"], data["empId"], data["department"], data["date"])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/employees")
def get_employees():
    conn = get_db()
    rows = conn.execute("SELECT * FROM employees ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ---------- FRONTEND ----------
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    app.run(debug=True)