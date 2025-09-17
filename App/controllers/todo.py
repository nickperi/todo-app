import calendar
from datetime import date, datetime

from sqlalchemy import func
from App.models import Todo, Student, User
from App.database import db


def create_todo(text, user_id, date_due, category):

    student = Student.query.filter_by(id=user_id).first()

    if not student:
        return None
    
    todo = Todo.query.filter_by(user_id=user_id, text=text).first()

    if not todo:
        new_todo = student.add_todo(text=text, date_due=date_due, category=category)
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

        if todo.done:
            todo.date_completed = datetime.now().strftime("%a, %b %d, %Y %I:%M %p")
        else:
            todo.date_completed = None
            
        db.session.add(todo)
        db.session.commit()
        return todo
    return None


def changeCategory(id, category):
    todo = get_todo(id)

    if todo:
        todo.category = category
        db.session.add(todo)
        db.session.commit()
        return todo
    return None



def get_all_todos():
    todos = Todo.query.order_by(Todo.id).all()
    return todos

def get_todos_by_month(user_id, month, year):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    todos = Todo.query.filter(Todo.date_due >= start_date,
                                 Todo.date_due <= end_date, Todo.user_id==user_id)
    return todos
    
def get_todos_by_month_json(user_id, month, year):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    todos = Todo.query.filter(Todo.date_due >= start_date,
                                 Todo.date_due <= end_date, Todo.user_id==user_id)
    todos = [todo.get_json() for todo in todos]
    return todos
    

def get_todos_by_due_date(user_id, year, month, day):
    #date_object = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
    date_object = date(year, month, day)
    todos = Todo.query.filter(func.date(Todo.date_due) == date_object, Todo.user_id==user_id).all()
    return todos

def get_todos_by_due_date_json(user_id, year, month, day):
    #date_object = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
    date_object = date(year, month, day)
    todos = Todo.query.filter(func.date(Todo.date_due) == date_object, Todo.user_id==user_id).all()
    todos = [todo.get_json() for todo in todos]
    return todos

def sort_todos_by_date_created(user_id):
    todos = Todo.query.filter_by(user_id=user_id).order_by(Todo.date_created).all()
    todos = [todo.get_json() for todo in todos]
    return todos

def sort_todos_by_date_due(user_id):
    todos = Todo.query.filter_by(user_id=user_id).order_by(Todo.date_due).all()
    todos = [todo.get_json() for todo in todos]
    return todos
    

def get_all_todos_json(user_id):
    todos = Todo.query.filter_by(user_id=user_id).order_by(Todo.id).all()

    if not todos:
        return []
    
    todos = [todo.get_json() for todo in todos]
    return todos

def calculate_time_elapsed(date_due, date_created):
    diff = date_due - date_created
    seconds = diff.total_seconds()

    if(seconds < 60):
        return f"{int(seconds)}s"
    elif(seconds < 3600):
        return f"{int(seconds//60)}m"
    elif(seconds < 86400):
        return f"{int(seconds//3600)}h"
    elif(seconds < 604800):
        return f"{int(seconds//86400)}d"
    elif(seconds < 2419200):
        return f"{int(seconds//604800)}w"
    else:
        return f"{diff}"
    
def get_custom_todos(user_id, sort, category, date_due, status):
    query = Todo.query
    
    if sort:
        if sort == 'date-due':
            query = query.filter_by(user_id=user_id).order_by(db.desc(Todo.date_due))
        elif sort == 'date-created':
            query.filter_by(user_id=user_id).order_by(Todo.date_created)

    if category:
        query = query.filter_by(user_id=user_id, category=category)

    if date_due:
        date_values = date_due.split('-')
        year = date_values[0]
        month = date_values[1]
        day = date_values[2]
        date_object = date(year, month, day)
        query = query.filter(func.date(Todo.date_due) == date_object, Todo.user_id==user_id)

    if status:
        query = query.filter_by(user_id=user_id, done=False)
    
    todos = query.all()
    todos = [todo.get_json() for todo in todos]
    return todos