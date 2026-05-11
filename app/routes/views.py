from flask import Blueprint, render_template
from flask_login import login_required, current_user

views_bp = Blueprint('views', __name__)

# Main Dashboard Route (Login required)
@views_bp.route('/')
@login_required
def index():
    return render_template('index.html')

# Login Page Route
@views_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('login.html')

# Register Page Route
@views_bp.route('/register')
def register():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('register.html')