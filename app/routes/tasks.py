from flask import Blueprint, request, jsonify
from app import db, socketio  # <-- socketio yahan add kiya hai
from app.models import Task
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
        
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'Medium'),
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    
    # WebSocket Event Fire kiya (Real-time update ke liye)
    socketio.emit('task_updated', {'msg': 'Naya task add hua hai!'})
    
    return jsonify({'message': 'Task added successfully', 'task': new_task.to_dict()}), 201

@tasks_bp.route('/api/tasks/<int:id>', methods=['PUT'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized action'}), 403
        
    data = request.get_json()
    task.status = data.get('status', task.status)
    db.session.commit()
    
    # WebSocket Event Fire kiya
    socketio.emit('task_updated', {'msg': 'Task ka status update hua!'})
    
    return jsonify({'message': 'Task updated successfully'}), 200

@tasks_bp.route('/api/tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized action'}), 403
        
    db.session.delete(task)
    db.session.commit()
    
    # WebSocket Event Fire kiya
    socketio.emit('task_updated', {'msg': 'Task delete ho gaya!'})
    
    return jsonify({'message': 'Task deleted successfully'}), 200