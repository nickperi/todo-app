from datetime import date, datetime

from sqlalchemy import func
from App.models import Todo, Student, User
from App.database import db


def create_todo(text, user_id, date_due):

    student = Student.query.filter_by(id=user_id).first()

    if not student:
        return None
    
    todo = Todo.query.filter_by(user_id=user_id, text=text).first()

    if not todo:
        new_todo = student.add_todo(text=text, date_due=date_due)
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

def toggle_todo(id):
    todo = get_todo(id)

    if todo:
        todo.done = not todo.done
        db.session.add(todo)
        db.session.commit()
        return todo
    return None


def get_all_todos():
    todos = Todo.query.order_by(Todo.id).all()
    return todos

def get_todos_by_month(month, year):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, 31, 23, 59, 59)
    todos = Todo.query.filter(Todo.date_due >= start_date,
                                 Todo.date_due <= end_date).all()
    return todos
    
def get_todos_by_month_json(month, year):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, 31, 23, 59, 59)
    todos = Todo.query.filter(Todo.date_due >= start_date,
                                 Todo.date_due <= end_date).all()
    todos = [todo.get_json() for todo in todos]
    return todos
    

def get_todos_by_due_date(year, month, day):
    #date_object = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
    date_object = date(year, month, day)
    todos = Todo.query.filter(func.date(Todo.date_due) == date_object).all()
    return todos
    

def get_all_todos_json():
    todos = Todo.query.all()

    if not todos:
        return []
    
    todos = [todo.get_json() for todo in todos]
    return todos