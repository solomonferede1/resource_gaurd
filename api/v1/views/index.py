#!/usr/bin/python3
"""module index - main view"""

from models.employee import Employee
from models.attendance import Attendance
from models.payroll import Payroll
from models.catagory import Catagory
from models.product import Product
from models.supplier import Supplier
from models.raw_material import RawMaterial
from models.product_transaction import ProductTransaction
from models.raw_material_transaction import RawMaterialTransaction
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status")
def status():
    return jsonify({"status" : "Ok"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """ Retrieves the number of each objects by type """

    classes = {'Employee' : Employee, 'Attendance' : Attendance,
               'Payroll' : Payroll, 'Catagory' : Catagory,'Product' : Product,
               'Supplier' : Supplier, 'RawMaterial' : RawMaterial,
               'ProductTransaction' : ProductTransaction,
               'RawMaterialTransaction' : RawMaterialTransaction}

    num_objs = {}
    for key, value in classes.items():
        num_objs[key] = storage.count(value)

    return jsonify(num_objs)