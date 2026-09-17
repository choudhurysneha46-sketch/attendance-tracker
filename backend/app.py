from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # allows frontend (different domain) to talk to this backend

DB_PATH = os.path.join(os.path.dirname(__file__), "attendance.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            total_classes INTEGER NOT NULL DEFAULT 0,
            attended_classes INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "Attendance Tracker API is running"})


# Get all subjects with their attendance %
@app.route("/api/subjects", methods=["GET"])
def get_subjects():
    conn = get_db()
    rows = conn.execute("SELECT * FROM subjects").fetchall()
    conn.close()

    subjects = []
    for row in rows:
        total = row["total_classes"]
        attended = row["attended_classes"]
        percentage = round((attended / total) * 100, 2) if total > 0 else 0
        subjects.append({
            "id": row["id"],
            "name": row["name"],
            "total_classes": total,
            "attended_classes": attended,
            "percentage": percentage
        })
    return jsonify(subjects)


# Add a new subject
@app.route("/api/subjects", methods=["POST"])
def add_subject():
    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Subject name is required"}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO subjects (name, total_classes, attended_classes) VALUES (?, 0, 0)",
            (name,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Subject already exists"}), 400
    conn.close()
    return jsonify({"message": "Subject added"}), 201


# Log a class (present or absent) for a subject
@app.route("/api/subjects/<int:subject_id>/log", methods=["POST"])
def log_class(subject_id):
    data = request.get_json()
    present = data.get("present", False)

    conn = get_db()
    if present:
        conn.execute(
            "UPDATE subjects SET total_classes = total_classes + 1, "
            "attended_classes = attended_classes + 1 WHERE id = ?",
            (subject_id,)
        )
    else:
        conn.execute(
            "UPDATE subjects SET total_classes = total_classes + 1 WHERE id = ?",
            (subject_id,)
        )
    conn.commit()
    conn.close()
    return jsonify({"message": "Class logged"})


# Delete a subject
@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    conn = get_db()
    conn.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Subject deleted"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0",
            port=int(os.environ.get("PORT",5000)))
    
