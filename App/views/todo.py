from flask import Blueprint, json, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime

from.index import index_views

from App.controllers import (
    create_todo,
    get_all_users,
    get_all_students,
    get_todo,
    update_todo,
    toggle_todo,
    changeCategory,
    get_all_todos,
    get_todos_by_due_date,
    get_todos_by_month_json,
    get_todos_by_month,
    get_all_todos_json,
    calculate_time_elapsed,
    jwt_required
)



todo_views = Blueprint('todo_views', __name__, template_folder='../templates')

'''@todo_views.route('/dashboard')
@jwt_required()
def display_dashboard():
    users = get_all_users()
    students = get_all_students()
    message=f"You are logged in as {current_user.id} - {current_user.username}"
    todos = get_todos_by_month(month=datetime.now().month, year=datetime.now().year)
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return render_template('dashboard.html', active_tab='todos-calendar', users=users, students=students, message=message, todos=todos, current_user=current_user, months=months, month=datetime.now().month, year=datetime.now().year, day=datetime.now().day)
'''


@todo_views.route('/todos', methods=['GET'])
@jwt_required()
def get_todo_page():
    todos = get_all_todos()
    return render_template('todos.html', todos=todos, current_user=current_user)


@todo_views.route('/todos/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def get_todos(year, month):
    todos = get_todos_by_month_json(current_user.id, month, year)
    return jsonify(todos)


@todo_views.route('/todos/<string:year_month_day>', methods=['GET'])
@jwt_required()
def get_todos_by_date(year_month_day):
    date_values = year_month_day.split('_')
    year = int(date_values[0])
    month = int(date_values[1])
    day = int(date_values[2])
    todos = get_todos_by_due_date(current_user.id, year, month, day)
    return render_template('todos.html', calculate_time_elapsed=calculate_time_elapsed, date=datetime(year, month, day), todos=todos, current_user=current_user, year=year, month=month, day=day, hour=datetime.now().hour, minute=datetime.now().minute)

@todo_views.route('/todos/<string:year_month_day>', methods=['POST'])
@jwt_required()
def create_todo_action(year_month_day):
    data = request.form
    due_date = data['due-date']
    due_time = data['due-time']
    due_date_time = f"{due_date} {due_time}"
    dt = datetime.strptime(due_date_time, "%Y-%m-%d %H:%M")
    todo = create_todo(data['text'], current_user.id, dt, data['category'])

    if todo:
        flash(f"Todo {todo.id} created by User {current_user.id} due on {due_date} at {due_time}!")
    else:
        flash(f"Failed to create todo !")

    return redirect(url_for('todo_views.get_todos_by_date', year_month_day=year_month_day))


@todo_views.route('/todos-calendar', methods=['GET'])
@jwt_required()
def show_todos_for_month():
    todos = get_todos_by_month(current_user.id, month=datetime.now().month, year=datetime.now().year)
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return render_template('calendar.html', todos=todos, current_user=current_user, months=months, month=datetime.now().month, year=datetime.now().year, day=datetime.now().day, active_tab='todos-calendar')


@todo_views.route('/todos/<int:id>', methods=['GET'])
def get_todo_page_by_id(id):
    todo = get_todo(id)
    return render_template('todo.html', todo=todo)


@todo_views.route('/todos/<int:id>', methods=['PUT'])
def update_todo_action(id):
    data = request.json
    todo = update_todo(id, data['text'])
    flash(f"Todo {todo.id} updated!")
    return jsonify({'success':True, 'text':data['text']})

@todo_views.route('/todos/<int:id>/check', methods=['PUT'])
def toggle_todo_action(id):
    todo = toggle_todo(id)

    if todo.done:
        date_completed = todo.date_completed.strftime("%a, %b %d, %Y %I:%M %p")
        flash(f"Todo {todo.id} marked as done!")
        return jsonify({'success':True, 'done':todo.done, 'date_completed':date_completed, 'time_taken':calculate_time_elapsed(todo.date_completed, todo.date_created)})
    else:
        date_completed = None
        flash(f"Todo {todo.id} marked as incomplete!")      
        return jsonify({'success':True, 'done':todo.done})


@todo_views.route('/todos/<int:id>/change-category', methods=['PUT'])
def change_category_action(id):
    data = request.json
    todo = changeCategory(id, data['category'])
    
    flash(f"Todo {todo.id} category changed to {data['category']}!")      
    return jsonify({'success':True, 'category':data['category']})


@todo_views.route('/api/todos', methods=['GET'])
def get_todos_action():
    todos = get_all_todos_json()
    return jsonify(todos)

@todo_views.route('/api/todos', methods=['POST'])
def create_todo_endpoint():
    data = request.json

    todo = create_todo(data['text'], data['user_id'])

    if not todo:
        return jsonify({'message': f"failed to create todo"})
    
    return jsonify({'message': f"todo {todo.text} created with id {todo.id}"})

