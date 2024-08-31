#!/usr/bin/python3
"""Attendance API"""

from models import storage
from models.attendance import Attendance
from models.employee import Employee
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/attendances/', methods=['GET'], strict_slashes=False)
def get_attendances():
    '''Retrieve all employees'''
    all_attendances = storage.all(Attendance).values()
    return jsonify([attendance.to_dict() for attendance in all_attendances])


@app_views.route('/employees/<employee_id>/attendance', methods=['GET'], strict_slashes=False)
def get_attendances_employee_id(employee_id):
    """Retrieves an Employee object"""
    employee = storage.get(Employee, int(employee_id))
    if not employee:
        abort(404)

    return jsonify([attendance.to_dict() for attendance in employee.attendances])


@app_views.route('/attendances/<attendance_id>', methods=['DELETE'], strict_slashes=False)
def delete_attendance(attendance_id):
    """Deletes an Employee object"""
    attendance = storage.get(Attendance, int(attendance_id))
    if not attendance:
        abort(404)
    storage.delete(attendance)
    storage.save()
    return jsonify({}), 200


@app_views.route('/attendances', methods=['POST'], strict_slashes=False)
def create_attendance():
    """Creates an attendance"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'employee_id' not in data:
        abort(400, description="Missing employee id")
    attendance = Attendance(**data)
    storage.new(attendance)
    storage.save()
    return jsonify(attendance.to_dict()), 201


@app_views.route('/attendances/<attendance_id>', methods=['PUT'], strict_slashes=False)
def update_attendance(attendance_id):
    """Updates attendance object"""
    attendance = storage.get(Attendance, int(attendance_id))
    if not attendance:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(attendance, key, value)
    storage.save()
    return jsonify(attendance.to_dict()), 200
