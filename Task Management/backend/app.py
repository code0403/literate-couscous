# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from database import get_mongo_connection
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin 

app.config['MONGO_URI'] = 'mongodb://localhost:27017/taskdb'  # Replace with your MongoDB URI
mongo = PyMongo(app, resources={r"/*": {"origins": "*"}})

# Test route
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = mongo.db.tasks.find()
    result = []
    for task in tasks:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string for JSON serialization
        result.append(task)
    return jsonify(result), 200


# Route to get a single task by ID
@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        task['_id'] = str(task['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(task), 200
    return jsonify({'message': 'Task not found'}), 404


# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False)
    if title and description:
        task_id = mongo.db.tasks.insert_one({
            'title': title,
            'description': description,
            'completed': completed
        }).inserted_id
        return jsonify({'message': 'Task created successfully', 'id': str(task_id)}), 201
    return jsonify({'message': 'Title and description are required'}), 400



# Route to update a task by ID
@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False)
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {
            '$set': {
                'title': title,
                'description': description,
                'completed': completed
            }
        })
        return jsonify({'message': 'Task updated successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404



# Route to delete a task by ID
@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    if task:
        mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404



# Define other routes here...

if __name__ == '__main__':
    app.run(debug=True)

