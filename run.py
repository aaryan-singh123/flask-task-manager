from app import create_app, db, socketio
from app.models import User, Task

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables connected and checked successfully!")

if __name__ == '__main__':
    socketio.run(app, debug=True)