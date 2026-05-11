from flask import Blueprint, request, jsonify
from app import db  # <-- Yeh line theek kar di gayi hai
from app.models import User
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

# 1. User Registration API
@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    new_user = User(username=data['username'])
    new_user.set_password(data['password']) 
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# 2. User Login API
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and user.check_password(data.get('password')):
        login_user(user) 
        return jsonify({'message': 'Logged in successfully', 'username': user.username}), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

# 3. User Logout API
@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user() 
    return jsonify({'message': 'Logged out successfully'}), 200