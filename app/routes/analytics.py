from flask import Blueprint, jsonify
from app.models import Task
from flask_login import login_required, current_user
import pandas as pd
import numpy as np

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    # User ke saare tasks fetch karo
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Agar user ka koi task nahi hai, toh sab 0 return karo
    if not tasks:
        return jsonify({
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'completion_percentage': 0.0
        }), 200

    # Tasks ko Pandas DataFrame mein convert karne ke liye list of dicts banaye
    task_list = [task.to_dict() for task in tasks]
    df = pd.DataFrame(task_list)
    
    # Pandas ka use karke metrics calculate karo
    total_tasks = int(len(df))
    
    # Check karo ki 'status' column mein data hai ya nahi
    if 'status' in df.columns:
        completed_tasks = int(len(df[df['status'] == 'Completed']))
        pending_tasks = int(len(df[df['status'] == 'Pending']))
    else:
        completed_tasks = 0
        pending_tasks = 0
    
    # NumPy ka use karke percentage nikalo aur 2 decimal tak round off karo
    if total_tasks > 0:
        # np.round use kiya hai jo specifically requirement mein pucha ja sakta hai
        percentage = np.round((completed_tasks / total_tasks) * 100, 2)
    else:
        percentage = 0.0
        
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': float(percentage)
    }), 200