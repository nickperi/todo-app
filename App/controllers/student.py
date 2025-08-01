from App.models import Student
from App.database import db

def create_student(username, password, email):
    newuser = Student(username=username, password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_all_students():
    students = Student.query.all()
    return students

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students