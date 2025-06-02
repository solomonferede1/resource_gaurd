#!/usr/bin/python3
"""Main application file with Employee-based authentication"""

from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import storage
from models.employee import Employee
from models.product import Product
from models.raw_material import RawMaterial
from models.category import Category
from models.supplier import Supplier
from web_dynamic.forms import RegistrationForm, LoginForm
from math import ceil
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


app = Flask(__name__)

app.config['SECRET_KEY'] = '5c74307621529bb8e56d8d8a46c058d92e07f804a0befdc7e4ee2fe6c16593aa'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Bonvolu ensaluti por uzi tiun paĝon."


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return storage.get(Employee, user_id)


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():
    return render_template('landing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if email already exists
        if storage.find_employee_by_email(form.email.data):
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
            
        # Create new employee
        new_employee = Employee(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            department=form.department.data,
            role=form.role.data,
            status='active'
        )
        storage.new(new_employee)
        storage.save()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('employee'))
        
    form = LoginForm()
    if form.validate_on_submit():
        employee = storage.find_employee_by_email(form.email.data)
        
        if employee and check_password_hash(employee.password, form.password.data):
            if employee.status != 'active':
                flash('Your account is inactive', 'danger')
                return redirect(url_for('login'))
                
            login_user(employee, remember=form.remember.data)
            flash(f'Login successfull, {employee.first_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('employee'))
            
        flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/employees', strict_slashes=False)
@login_required
def employee():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Items per page
    
    # Sorting parameters
    sort_by = request.args.get('sort_by', 'first_name')
    sort_order = request.args.get('sort_order', 'asc')
    
    # Filter parameters
    department = request.args.get('department', '')
    search_term = request.args.get('search', '')
    
    storage.reload() 
    all_employees_from_storage = storage.all(Employee).values()
    
    filtered_employees = []
    for emp in all_employees_from_storage:
        if department and emp.department != department:
            continue
            
        if search_term:
            search_lower = search_term.lower()
            if not (search_lower in emp.first_name.lower() or 
                    search_lower in emp.last_name.lower() or 
                    search_lower in emp.email.lower() or 
                    search_lower in emp.role.lower()):
                continue
                
        filtered_employees.append(emp)
    
    reverse_order = (sort_order == 'desc')
    filtered_employees.sort(
        key=lambda x: getattr(x, sort_by, x.first_name),
        reverse=reverse_order
    )

    total_employees = len(filtered_employees)
    total_pages = ceil(total_employees / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_employees = filtered_employees[start_idx:end_idx]
    
    left_edge = 2
    left_current = 2
    right_current = 5
    right_edge = 2
    
    page_numbers = []
    last_page = 0
    
    for num in range(1, total_pages + 1):
        if (num <= left_edge or 
            (num > page - left_current - 1 and num < page + right_current) or 
            num > total_pages - right_edge):
            if last_page + 1 != num:
                page_numbers.append(None)
            page_numbers.append(num)
            last_page = num
    
    return render_template(
        'employee.html',
        employees=paginated_employees,
        pagination={
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total_employees,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_num': page - 1,
            'next_num': page + 1,
            'iter_pages': page_numbers,
            'current_page': page
        },
        current_sort=sort_by,
        current_order=sort_order,
        current_department=department,
        current_search=search_term
    )

@app.route('/get_edit_form')
@login_required
def get_edit_form():
    return render_template('edit_employee_form.html')

@app.route('/add_employee', strict_slashes=False)
@login_required
def add_employee():
    return render_template('add_employee.html')

@app.route('/products', strict_slashes=False)
@login_required
def product():
    products = storage.all(Product).values()
    categories = storage.all(Category).values()
    if products:
        return render_template('product.html', products=products, categories=categories)


@app.route('/filter_products_by_category', methods=['GET'])
def filter_products_by_category():
    category_id = request.args.get('category_id')

    if category_id == "all" or category_id:
        products = [product.to_dict() for product in storage.all(Product).values()]
    else:
        products = storage.products_filter_by_category(category_id)
    print(products)
    print(jsonify(products))
    return jsonify(products=products)



@app.route('/add_product', strict_slashes=False)
@login_required
def add_product():
    categories = storage.all(Category).values()
    if categories:
        return render_template('add_product.html', categories=categories)

@app.route('/rawmaterials', strict_slashes=False)
@login_required
def raw_material():
    raw_materials = storage.all(RawMaterial).values()
    if raw_materials:
        return render_template('raw_material.html', raw_materials=raw_materials)

@app.route('/add_raw_material', strict_slashes=False)
@login_required
def add_raw_material():
    suppliers = storage.all(Supplier).values()
    if suppliers:
        return render_template('add_raw_material.html', suppliers=suppliers)

@app.route('/transactions', strict_slashes=False)
@login_required
def transaction():
    return render_template('transaction.html')

@app.route('/inventories', strict_slashes=False)
@login_required
def inventory():
    storage.reload() 
    raw_materials = storage.all(RawMaterial).values()
    products = storage.all(Product).values()
    employees = storage.all(Employee).values()

    total_raw_materials = sum(rm.quantity for rm in raw_materials)
    total_products = sum(p.quantity for p in products)
    total_employees = len(employees) 

    return render_template(
        'inventory.html',
        total_raw_materials=total_raw_materials,
        total_products=total_products,
        total_employees=total_employees
    )

if __name__ == "__main__":
    app.run(host='localhost', port='5050')