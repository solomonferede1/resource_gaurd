#!/usr/bin/python3
"""Employee"""


from flask import Flask, render_template
from models import storage
from models.employee import Employee
from models.product import Product
from models.raw_material import RawMaterial
from models.supplier import Supplier


app = Flask(__name__)


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/home')
@app.route('/')
def home():

    return render_template('home.html')


@app.route('/employees')
def employees():

    employees = storage.all(Employee).values()
    if employees:
        return render_template('employee.html', employees=employees)


@app.route('/add_employee')
def add_employee():

    return render_template('add_employee.html')


@app.route('/products')
def products():

    products= storage.all(Product).values()
    if products:
        return render_template('product.html', products=products)


@app.route('/rawmaterials')
def rawmaterials():

    raw_materials= storage.all(RawMaterial).values()
    suppliers = storage.all(Supplier).values()
    if raw_materials:
        return render_template('raw_material.html', raw_materials=raw_materials, suppliers=suppliers)


if __name__ == "__main__":
    app.run(host='localhost', port='5050')
