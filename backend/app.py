from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage (replaces MySQL)
tasks = [
    {"id": 1, "title": "Test task 1"},
    {"id": 2, "title": "Test task 2"}
]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route('/add', methods=['POST'])
def add_task():
    data = request.json
    title = data.get('title')

    # generate new ID
    new_id = tasks[-1]["id"] + 1 if tasks else 1

    # create new fake task
    new_task = {"id": new_id, "title": title}
    tasks.append(new_task)

    return jsonify({"message": "Task added!", "task": new_task}), 201

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]

    return jsonify({"message": "Task deleted!", "deleted_id": task_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
