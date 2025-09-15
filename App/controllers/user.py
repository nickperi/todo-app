from App.models import User
from App.database import db
from sqlalchemy.exc import PendingRollbackError

def create_user(username, password):
    newuser = User(username=username, password=password)

    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except PendingRollbackError:
        # Handle the PendingRollbackError
        print("PendingRollbackError encountered. Rolling back session.")
        db.session.rollback()
    except Exception as e:
        # Handle other potential exceptions during the operation
        print(f"An unexpected error occurred: {e}")
        db.session.rollback() # Ensure rollback for other errors too
    finally:
        # It's generally good practice to close the session when done
        db.session.close()
        if newuser:
            return newuser
        else:
            return None
        # Or handle session closing elsewhere in your application lifecycle

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    