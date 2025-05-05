from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task
from app.schemas import TaskSchema

task_bp = Blueprint('tasks', __name__)
task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

# ✅ Create a new task
@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    errors = task_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()
    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        user_id=user_id
    )
    try:
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500

# 📖 Get all tasks of the logged-in user
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return task_list_schema.dump(tasks), 200

# 🔎 Get one task by ID
@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return task_schema.dump(task), 200

# ✏️ Update a task
@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    errors = task_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(task, key, value)

    db.session.commit()
    return task_schema.dump(task), 200

# ❌ Delete a task
@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

# ✅ Mark as complete/incomplete
@task_bp.route('/tasks/<int:task_id>/toggle', methods=['PATCH'])
@jwt_required()
def toggle_task_completion(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task.is_completed = not task.is_completed
    db.session.commit()
    return jsonify({'message': 'Task status updated', 'is_completed': task.is_completed}), 200
