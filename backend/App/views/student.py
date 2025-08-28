from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_student,
    get_all_students,
    get_all_students_json,
    jwt_required
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/students', methods=['GET'])
def get_student_page():
    students = get_all_students()
    year_month_day = f"{datetime.now().year}_{datetime.now().month}_{datetime.now().day}"
    return render_template('students.html', students=students, year_month_day=year_month_day, active_tab='students')

@student_views.route('/students', methods=['POST'])
def create_student_action():
    data = request.form
    flash(f"Student {data['username']} created!")
    create_student(data['username'], data['password'], data['email'])
    return redirect(url_for('student_views.get_student_page'))

@student_views.route('/api/students', methods=['GET'])
def get_students_action():
    students = get_all_students_json()
    return jsonify(students)

@student_views.route('/api/students', methods=['POST'])
def create_student_endpoint():
    data = request.json
    student = create_student(data['username'], data['password'], data['email'])
    return jsonify({'message': f"student {student.username} created with id {student.id}"})

