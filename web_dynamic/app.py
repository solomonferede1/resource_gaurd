#!/usr/bin/python3
"""Main application file defining routes """


from flask import Flask, render_template, flash, redirect, url_for, request
from models import storage
from models.employee import Employee
from models.product import Product
from models.raw_material import RawMaterial
from models.catagory import Catagory
from models.supplier import Supplier
from web_dynamic.forms import RegistrationForm, LoginForm
from math import ceil


app = Flask(__name__)

app.config['SECRET_KEY'] = 'e8d8e819b162179bdabd44c318f13054'


@app.route('/', strict_slashes=False)
@app.route('/home', strict_slashes=False)
def home():

    return render_template('langing.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
            flash(f'You have been loged in', 'success')
            return redirect(url_for('employee'))
        else:
            flash(f'Login unsecussful, please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/employees', strict_slashes=False)
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
    
    # Get all employees
    all_employees = storage.all(Employee).values()
    
    # Apply filters
    filtered_employees = []
    for emp in all_employees:
        # Department filter
        if department and emp.department != department:
            continue
            
        # Search filter (name, email, or role)
        if search_term:
            search_lower = search_term.lower()
            if not (search_lower in emp.first_name.lower() or 
                    search_lower in emp.last_name.lower() or 
                    search_lower in emp.email.lower() or 
                    search_lower in emp.role.lower()):
                continue
                
        filtered_employees.append(emp)
    
    # Apply sorting
    reverse_order = (sort_order == 'desc')
    filtered_employees.sort(
        key=lambda x: getattr(x, sort_by, x.first_name),
        reverse=reverse_order
    )

    # Pagination logic
    total_employees = len(filtered_employees)
    total_pages = ceil(total_employees / per_page)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_employees = filtered_employees[start_idx:end_idx]
    
    # Generate page numbers for pagination
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
                page_numbers.append(None)  # Ellipsis marker
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
def get_edit_form():
    return render_template('edit_employee_form.html')

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

    raw_materials = storage.all(RawMaterial).values()
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

    raw_materials = storage.all(RawMaterial).values()
    products = storage.all(Product).values()
    employees = storage.all(Employee).values()

    # Calculate totals
    total_raw_materials = sum(rm.quantity for rm in raw_materials)
    total_products = sum(p.quantity for p in products)
    total_employees = len(employees)

    # Pass totals to the template
    return render_template(
        'inventory.html',
        total_raw_materials=total_raw_materials,
        total_products=total_products,
        total_employees=total_employees
    )


if __name__ == "__main__":
    app.run(host='localhost', port='5050')
