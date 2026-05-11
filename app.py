from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    database_url = "sqlite:///tasks.db"

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print("DATABASE_URL =", database_url)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({
        "message": "Flask Railway Running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

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

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    task = Task(title=data["title"])

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)