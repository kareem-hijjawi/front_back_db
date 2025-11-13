from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="todo_db"
    )

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "title": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/add', methods=['POST'])
def add_task():
    data = request.json
    title = data.get('title')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task added!"}), 201

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Task deleted!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
