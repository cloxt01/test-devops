import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# load env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def init_db():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        conn.commit()
    conn.close()


@app.route("/health")
def health():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
        conn.close()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 503


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks ORDER BY id;")
        rows = cur.fetchall()
    conn.close()
    return jsonify(rows), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING *;", (title,)
        )
        row = cur.fetchone()
        conn.commit()
    conn.close()
    return jsonify(row), 201

# init db saat startup
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", "8000")))
