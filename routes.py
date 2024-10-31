from flask import Blueprint, request, jsonify, abort
from models import db, Todo

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if not data or 'task' not in data:
        abort(400, description="Task field is required.")
    
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'id': new_todo.id, 'task': new_todo.task, 'completed': new_todo.completed}), 201

@todos_bp.route('/todos', methods=['GET'])
def get_all_todos():
    todos = Todo.query.all()
    return jsonify([{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos])

@todos_bp.route('/todos/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    todo = Todo.query.get_or_404(id)
    return jsonify({'id': todo.id, 'task': todo.task, 'completed': todo.completed})

@todos_bp.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    if 'task' in data:
        todo.task = data['task']
    if 'completed' in data:
        todo.completed = data['completed']
    
    db.session.commit()
    return jsonify({'id': todo.id, 'task': todo.task, 'completed': todo.completed})

@todos_bp.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully.'}), 204
