from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_todo,
    get_todo,
    update_todo,
    get_all_todos,
    get_all_todos_json,
    jwt_required
)



todo_views = Blueprint('todo_views', __name__, template_folder='../templates')

@jwt_required()
@todo_views.route('/todos', methods=['GET'])
def get_todo_page():
    todos = get_all_todos()
    return render_template('todos.html', todos=todos, current_user=jwt_current_user)

@jwt_required()
@todo_views.route('/todos', methods=['POST'])
def create_todo_action():
    data = request.form
    todo = create_todo(data['text'], jwt_current_user.id)
    flash(f"Todo {todo.id} created by User {{jwt_current_user.id}}!")
    return redirect(url_for('todo_views.get_todo_page'))

@todo_views.route('/todos/<int:id>', methods=['GET'])
def get_todo_page_by_id(id):
    todo = get_todo(id)
    return render_template('todo.html', todo=todo)

@todo_views.route('/todos/<int:id>', methods=['UPDATE'])
def update_todo_action(id):
    data = request.json
    todo = update_todo(id, data['text'])
    flash(f"Todo {todo.id} updated!")
    return jsonify({'success':True, 'text':data['text']})


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

