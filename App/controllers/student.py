from App.models import Student
from App.database import db
from sqlalchemy.exc import PendingRollbackError

def create_student(username, password, email):

    try:
        newuser = Student(username=username, password=password, email=email)
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

def get_all_students():
    students = Student.query.all()
    return students

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students