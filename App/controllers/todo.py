from App.models import Todo, Student
from App.database import db


def create_todo(text, user_id):

    students = Student.query.all()

    res = None
    for student in students:
        if student.id == user_id:
            res = student

    if not res:
        return None
    
    else:
        #new_todo = Todo(text=text, user_id=user_id)
        new_todo = res.add_todo(text=text)
        return new_todo

def get_all_todos():
    todos = Todo.query.all()
    return todos

def get_all_todos_json():
    todos = Todo.query.all()

    if not todos:
        return []
    
    todos = [todo.get_json() for todo in todos]
    return todos