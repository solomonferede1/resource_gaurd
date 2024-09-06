#!/usr/bin/python3
"""Employee"""


from flask import Flask, render_template
from models import storage
from models.employee import Employee
from models.product import Product


app = Flask(__name__)


@app.route('/home')
def home():

    all_employee = storage.all(Employee).values()
    if all_employee:
        return render_template('employee.html', all_employee=all_employee)


@app.route('/employees')
def employees():

    all_employee = storage.all(Employee).values()
    if all_employee:
        return render_template('employee.html', all_employee=all_employee)

@app.route('/products')
def products():

    products= storage.all(Product).values()
    if products:
        return render_template('product.html', products=products)


if __name__ == "__main__":
    app.run(host='localhost', port='5050')
