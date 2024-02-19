
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/")
def home():
    return render_template("todo.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    tasks = load_tasks()
    new_task = request.json.get("task")
    if new_task:
        tasks.append({"id": len(tasks) + 1, "text": new_task, "done": False})
        save_tasks(tasks)
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(debug=True)