from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "taskdb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "password")
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks")
    tasks = [{"id": r[0], "title": r[1], "done": r[2]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id", (data["title"],))
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": task_id, "title": data["title"], "done": False}), 201

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return "", 204

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
