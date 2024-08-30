#!/usr/bin/python3
"""Employee API"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.employee import Employee


@app_views.route('/employees/', methods=['GET'], strict_slashes=False)
def get_employees():
    '''Retrieve all employees'''
    all_employees = storage.all(Employee).values()
    return jsonify([employee.to_dict() for employee in all_employees])


@app_views.route('/employees/<employee_id>', methods=['GET'], strict_slashes=False)
def get_employee(employee_id):
    """Retrieves an Employee object"""
    employee = storage.get(Employee, int(employee_id))
    if not employee:
        abort(404)
    return jsonify(employee.to_dict())


@app_views.route('/employees/<employee_id>', methods=['DELETE'], strict_slashes=False)
def delete_employee(employee_id):
    """Deletes an Employee object"""
    employee = storage.get(Employee, int(employee_id))
    if not employee:
        abort(404)
    storage.delete(employee)
    storage.save()
    return jsonify({}), 200


@app_views.route('/employees', methods=['POST'], strict_slashes=False)
def create_employee():
    """Creates an Employee"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'first_name' not in data:
        abort(400, description="Missing first name")
    if 'last_name' not in data:
        abort(400, description="Missing last name")
    employee = Employee(**data)
    storage.new(employee)
    storage.save()
    return jsonify(employee.to_dict()), 201


@app_views.route('/employees/<employee_id>', methods=['PUT'], strict_slashes=False)
def update_employee(employee_id):
    """Updates an Employee object"""
    employee = storage.get(Employee, int(employee_id))
    if not employee:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(employee, key, value)
    storage.save()
    return jsonify(employee.to_dict()), 200
