import os
from dotenv import load_dotenv
from flask import Blueprint, json, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from datetime import datetime

import requests

from.index import index_views

from App.controllers import (
    create_todo,
    get_todo,
    update_todo,
    toggle_todo,
    changeCategory,
    get_all_todos,
    get_todos_by_due_date,
    get_todos_by_due_date_json,
    get_todos_by_month_json,
    get_todos_by_month,
    get_all_todos_json,
    calculate_time_elapsed,
    jwt_required
)



todo_views = Blueprint('todo_views', __name__, template_folder='../templates')
load_dotenv()

@todo_views.route('/api/todos', methods=['GET'], strict_slashes=False)
def get_todos_action():
    todos = get_all_todos_json()
    return jsonify(todos)

'''@todo_views.route('/')
def todo_app_index():
    return send_from_directory('dist', 'index.html') '''



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
    year_month_day = f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}"
    return render_template('todos.html', year_month_day=year_month_day, calculate_time_elapsed=calculate_time_elapsed, date=datetime(year, month, day), todos=todos, current_user=current_user, year=year, month=month, day=day, hour=datetime.now().hour, minute=datetime.now().minute)


@todo_views.route('/api/todos/<string:year_month_day>', methods=['GET'])
@jwt_required()
def get_todos_by_date_action(year_month_day):
    date_values = year_month_day.split('_')
    year = int(date_values[0])
    month = int(date_values[1])
    day = int(date_values[2])
    todos = get_todos_by_due_date_json(current_user.id, year, month, day)
    return jsonify(todos)


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
        data_field_values = due_date.split('-')
        y = data_field_values[0]
        m = data_field_values[1]
        d = data_field_values[2]
    else:
        flash(f"Failed to create todo !")

    return redirect(url_for('todo_views.get_todos_by_date', year_month_day=str(y)+"_"+str(m)+"_"+str(d)))


@todo_views.route('/todos-calendar', methods=['GET'])
@jwt_required()
def show_todos_for_month():
    todos = get_todos_by_month(current_user.id, month=datetime.now().month, year=datetime.now().year)
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    year_month_day = f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}"
    return render_template('calendar.html', todos=todos, current_user=current_user, year_month_day=year_month_day, months=months, month=datetime.now().month, year=datetime.now().year, day=datetime.now().day, active_tab='todos-calendar')


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


@todo_views.route('/api/todos', methods=['POST'])
def create_todo_endpoint():
    data = request.json

    todo = create_todo(data['text'], data['user_id'])

    if not todo:
        return jsonify({'message': f"failed to create todo"})
    
    return jsonify({'message': f"todo {todo.text} created with id {todo.id}"})



HF_TOKEN = os.getenv('HF_TOKEN')
API_URL = os.getenv('API_URL')
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def safe_parse_ai_output(output):
    try:
        # Extract JSON part
        start = output.find("{")
        end = output.rfind("}") + 1
        json_str = output[start:end]
        data = json.loads(json_str)
    except Exception as e:
        print("AI JSON parse failed:", e)
        data = {
            "title": "",
            "due_date": None,
            "due_time": None,
            "category": ""
        }
    return data

@todo_views.route('/parse-todo', methods=['POST'])
def parse_todo():
    data = request.get_json()
    if not data or "command" not in data:
        return jsonify({"error": "Missing 'command' field"}), 400

    user_input = data["command"]
    
    response = query({
    "messages": [
        {
            "role": "user",
            "content": "Given that today's date is " + str(datetime.now().strftime("%a, %b %d, %Y")) + "Can you generate json only with the appropriate task_title, date_due (YYYY-MM-DD), time_due (HH:mm), category (personal, reminder, school, work, urgent, other) for the task " + user_input + "?"
        }
    ],
    "model": "openai/gpt-oss-20b:fireworks-ai"
})
    
    todo = safe_parse_ai_output(response["choices"][0]["message"]["content"])
    print(response["choices"][0]["message"])
    return jsonify(todo)


