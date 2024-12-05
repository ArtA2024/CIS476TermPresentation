from models import db, User
from app import app  # Ensure 'app' is correctly imported

with app.app_context():
    user = User.query.filter_by(email='ahachek@umich.edu').first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f"Deleted user with email: {user.email}")
    else:
        print("User not found.")
