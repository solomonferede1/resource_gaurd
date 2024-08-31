#!/usr/bin/python3
"""Payroll API"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.employee import Employee
from models.payroll import Payroll


@app_views.route('/payrolls/', methods=['GET'], strict_slashes=False)
def get_payrolls():
    '''Retrieve all payroll records'''
    all_payrolls = storage.all(Payroll).values()
    return jsonify([payroll.to_dict() for payroll in all_payrolls])


@app_views.route('/employees/<employee_id>/payrolls/', methods=['GET'], strict_slashes=False)
def get_employee_payrolls(employee_id):
    '''Retrieve all payroll records for a specific employee'''
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)
    return jsonify([payroll.to_dict() for payroll in employee.payrolls])


@app_views.route('/payrolls/<payroll_id>', methods=['GET'], strict_slashes=False)
def get_payroll(payroll_id):
    """Retrieves a Payroll object"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    return jsonify(payroll.to_dict())


@app_views.route('/payrolls/<payroll_id>', methods=['DELETE'], strict_slashes=False)
def delete_payroll(payroll_id):
    """Deletes a Payroll object"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    storage.delete(payroll)
    storage.save()
    return jsonify({}), 200


@app_views.route('/payrolls', methods=['POST'], strict_slashes=False)
def create_payroll():
    """Creates a Payroll record"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    
    if 'total_work_hours' not in data:
        abort(400, description="Missing total_work_hours")
    if 'salary' not in data:
        abort(400, description="Missing salary")
    if 'employee_id' not in data:
        abort(400, description="Missing employee_id")

    payroll = Payroll(**data)
    storage.new(payroll)
    storage.save()
    return jsonify(payroll.to_dict()), 201


@app_views.route('/payrolls/<payroll_id>', methods=['PUT'], strict_slashes=False)
def update_payroll(payroll_id):
    """Updates a Payroll record"""
    payroll = storage.get(Payroll, payroll_id)
    if not payroll:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(payroll, key, value)
    
    storage.save()
    return jsonify(payroll.to_dict()), 200
