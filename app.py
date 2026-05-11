from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# membaca file .env
load_dotenv()

app = Flask(__name__)

# ambil DATABASE_URL dari .env
database_url = os.getenv("DATABASE_URL")

# cek apakah terbaca
print("DATABASE_URL =", database_url)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# model database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

# endpoint home
@app.route("/")
def home():
    return jsonify({
        "message": "Flask API Running"
    })

# endpoint health check
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

# GET semua task
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    result = []

    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title
        })

    return jsonify(result)

# POST task baru
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    task = Task(title=data["title"])

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created"
    })

# DELETE task
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)

    if not task:
        return jsonify({
            "message": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted"
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)