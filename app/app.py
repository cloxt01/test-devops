import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


# =========================
# Prometheus Metrics
# =========================

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)


@app.before_request
def before_request():
    request.start_time = time.perf_counter()


@app.after_request
def after_request(response):
    if request.path != "/metrics":
        duration = time.perf_counter() - request.start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.path,
        ).observe(duration)

    return response


def get_conn():
    return psycopg2.connect(
        **DB_CONFIG,
        cursor_factory=RealDictCursor
    )


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
        return jsonify({
            "status": "error",
            "detail": str(e)
        }), 503


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
        return jsonify({
            "error": "title is required"
        }), 400

    conn = get_conn()

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING *;",
            (title,)
        )

        row = cur.fetchone()
        conn.commit()

    conn.close()

    return jsonify(row), 201


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


# Init database saat startup
init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("APP_PORT", "8000"))
    )