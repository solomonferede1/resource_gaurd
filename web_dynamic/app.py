#!/usr/bin/python3
"""Employee"""


from flask import Flask, render_template
from models import storage
from models.employee import Employee
from models.product import Product
from models.raw_material import RawMaterial
from models.catagory import Catagory
from models.supplier import Supplier

app = Flask(__name__)


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():

    return render_template('langing.html')


@app.route('/login', strict_slashes=False)
def login():

    return render_template('login.html')


@app.route('/employees', strict_slashes=False)
def employee():

    employees = storage.all(Employee).values()
    if employees:
        return render_template('employee.html', employees=employees)


@app.route('/add_employee', strict_slashes=False)
def add_employee():

    return render_template('add_employee.html')


@app.route('/products', strict_slashes=False)
def product():

    products= storage.all(Product).values()
    if products:
        return render_template('product.html', products=products)


@app.route('/add_product', strict_slashes=False)
def add_product():

    catagories = storage.all(Catagory).values()
    if catagories:
        return render_template('add_product.html', catagories=catagories)


@app.route('/rawmaterials', strict_slashes=False)
def raw_material():

    raw_materials= storage.all(RawMaterial).values()
    if raw_materials:
        return render_template('raw_material.html', raw_materials=raw_materials)


@app.route('/add_raw_material', strict_slashes=False)
def add_raw_material():

    suppliers = storage.all(Supplier).values()
    if suppliers:
        return render_template('add_raw_material.html', suppliers=suppliers)



@app.route('/transactions', strict_slashes=False)
def transaction():

    return render_template('transaction.html')


@app.route('/inventories', strict_slashes=False)
def inventory():

    return render_template('inventory.html')


if __name__ == "__main__":
    app.run(host='localhost', port='5050')
