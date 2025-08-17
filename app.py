import os
import logging
from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

# Logging setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DB_FILE = "database.db"

def init_db():
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                );
            """)
            conn.commit()
            logging.info("Database initialized.")

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        logging.warning("Invalid submission: Missing name or email.")
        return jsonify({"error": "Missing fields"}), 400

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()

    logging.info(f"User added: {name}, {email}")
    return jsonify({"message": "User saved successfully!"}), 201

@app.route("/health", methods=["GET"])
def health_check():
    logging.info("Health check requested.")
    return {"status": "ok"}, 200

@app.route("/users", methods=["GET"])
def get_all_users():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT id, name, email FROM users")
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in cursor.fetchall()]
        if users:
            logging.info(f"Users retrieved: {users}")
        else:
            logging.info("No users retrieved.")
    return jsonify({"users": users}), 200


if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(host="0.0.0.0", debug=True)
