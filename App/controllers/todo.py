from App.models import Todo, Student, User
from App.database import db


def create_todo(text, user_id):

    student = Student.query.filter_by(id=user_id).first()

    if not student:
        return None
    
    todo = Todo.query.filter_by(user_id=user_id, text=text).first()

    if not todo:
        new_todo = student.add_todo(text=text)
        return new_todo
    return None

def get_todo(id):
    return Todo.query.get(id)

def update_todo(id, text):
     todo = Todo.query.get(id)

     if todo:
         todo.text = text
         db.session.add(todo)
         db.session.commit()
         return todo
     return None

def get_all_todos():
    todos = Todo.query.all()
    return todos

def get_all_todos_json():
    todos = Todo.query.all()

    if not todos:
        return []
    
    todos = [todo.get_json() for todo in todos]
    return todosfrom App.models import Todo, Student
from App.database import db