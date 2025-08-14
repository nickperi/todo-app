from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from datetime import datetime

from.index import index_views

from App.controllers import (
    create_todo,
    get_todo,
    update_todo,
    toggle_todo,
    get_all_todos,
    get_todos_by_due_date,
    get_todos_by_month_json,
    get_todos_by_month,
    get_all_todos_json,
    jwt_required
)



todo_views = Blueprint('todo_views', __name__, template_folder='../templates')

@todo_views.route('/todos', methods=['GET'])
@jwt_required()
def get_todo_page():
    todos = get_all_todos()
    return render_template('todos.html', todos=todos, current_user=jwt_current_user)


@todo_views.route('/todos/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def get_todos(year, month):
    todos = get_todos_by_month_json(month, year)
    return jsonify(todos)


@todo_views.route('/todos/<string:year_month_day>', methods=['GET'])
@jwt_required()
def get_todos_by_date(year_month_day):
    date_values = year_month_day.split('_')
    year = int(date_values[0])
    month = int(date_values[1])
    day = int(date_values[2])
    todos = get_todos_by_due_date(year, month, day)
    return render_template('todos.html', todos=todos, current_user=jwt_current_user, year=year, month=month, day=day, hour=datetime.now().hour, minute=datetime.now().minute)

@todo_views.route('/todos/<string:year_month_day>', methods=['POST'])
@jwt_required()
def create_todo_action(year_month_day):
    data = request.form
    todo = create_todo(data['text'], jwt_current_user.id, data['date-time'])
    flash(f"Todo {todo.id} created by User {jwt_current_user.id}!")
    return redirect(url_for('todo_views.get_todos_by_date', year_month_day=year_month_day))


@todo_views.route('/todos-calendar', methods=['GET'])
@jwt_required()
def show_todos_for_month():
    todos = get_todos_by_month(month=datetime.now().month, year=datetime.now().year)
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return render_template('calendar.html', todos=todos, current_user=jwt_current_user, months=months, month=datetime.now().month, year=datetime.now().year, day=datetime.now().day)


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
        flash(f"Todo {todo.id} marked as done!")
    else:
        flash(f"Todo {todo.id} marked as incomplete!")
        
    return jsonify({'success':True, 'done':todo.done})


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

