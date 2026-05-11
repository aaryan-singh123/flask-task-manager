from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

# Environment variables load kar rahe hain .env file se
load_dotenv()

# Extensions initialize kar rahe hain
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    
    # App Configurations
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Extensions ko app ke sath link kar rahe hain
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Agar koi bina login kiye protected page pe jaye, toh usko kahan bhejna hai
    login_manager.login_view = 'views.login'
    login_manager.login_message_category = 'info'

    # Database model import aur User Loader setup
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Blueprints Registration (Saari APIs aur Routes ko app se jodna) ---
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.analytics import analytics_bp
    from app.routes.views import views_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(views_bp)

    return app