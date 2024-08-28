#!/usr/bin/python3

from models import storage
from models.employee import Employee
from models.attendance import Attendance
from models.payroll import Payroll
from models.catagory import Catagory
from models.product import Product
from datetime import date, datetime

# List of Employee objects
employees = [
    Employee(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", salary=5000),
    Employee(first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone="0987654321", salary=5500),
    Employee(first_name="Michael", last_name="Johnson", email="michael.johnson@example.com", phone="1122334455", salary=6000),
    Employee(first_name="Emily", last_name="Davis", email="emily.davis@example.com", phone="2233445566", salary=4800),
    Employee(first_name="Chris", last_name="Brown", email="chris.brown@example.com", phone="3344556677", salary=5200),
    Employee(first_name="Olivia", last_name="Taylor", email="olivia.taylor@example.com", phone="4455667788", salary=5700)
]

# Loop through each employee and save them to the database
for employee in employees:
    storage.new(employee)

attendances = [
    {'attendance_date': '2024-08-28', 'check_in_time': '2024-08-28 09:00:00', 'check_out_time': '2024-08-28 17:00:00', 'employee_id': 1},
    {'attendance_date': '2024-08-28', 'check_in_time': '2024-08-28 09:15:00', 'check_out_time': '2024-08-28 17:05:00', 'employee_id': 2},
    {'attendance_date': '2024-08-28', 'check_in_time': '2024-08-28 09:30:00', 'check_out_time': '2024-08-28 17:10:00', 'employee_id': 3},
    {'attendance_date': '2024-08-28', 'check_in_time': '2024-08-28 09:45:00', 'check_out_time': '2024-08-28 17:15:00', 'employee_id': 4},
    {'attendance_date': '2024-08-28', 'check_in_time': '2024-08-28 10:00:00', 'check_out_time': '2024-08-28 17:20:00', 'employee_id': 5},
    {'attendance_date': '2024-08-28', 'check_in_time': '2024-08-28 10:15:00', 'check_out_time': '2024-08-28 17:25:00', 'employee_id': 6}
]

# Insert attendance data
for data in attendances:
    attendance = Attendance(
        attendance_date=data['attendance_date'],
        check_in_time=data['check_in_time'],
        check_out_time=data['check_out_time'],
        employee_id=data['employee_id']
    )
    storage.new(attendance)


# Example payroll data to insert

payroll_data = [
    # August 2024 payroll
    {'total_work_hours': 160.00, 'salary': 5000.00, 'net_salary': 4500.00, 'payment_date': date(2024, 8, 28), 'employee_id': 1},
    {'total_work_hours': 160.00, 'salary': 5500.00, 'net_salary': 4950.00, 'payment_date': date(2024, 8, 28), 'employee_id': 2},
    {'total_work_hours': 160.00, 'salary': 6000.00, 'net_salary': 5400.00, 'payment_date': date(2024, 8, 28), 'employee_id': 3},
    {'total_work_hours': 160.00, 'salary': 4800.00, 'net_salary': 4320.00, 'payment_date': date(2024, 8, 28), 'employee_id': 4},
    {'total_work_hours': 160.00, 'salary': 5200.00, 'net_salary': 4680.00, 'payment_date': date(2024, 8, 28), 'employee_id': 5},
    {'total_work_hours': 160.00, 'salary': 5700.00, 'net_salary': 5130.00, 'payment_date': date(2024, 8, 28), 'employee_id': 6},

    # July 2024 payroll
    {'total_work_hours': 158.00, 'salary': 5000.00, 'net_salary': 4500.00, 'payment_date': date(2024, 7, 28), 'employee_id': 1},
    {'total_work_hours': 158.50, 'salary': 5500.00, 'net_salary': 4950.00, 'payment_date': date(2024, 7, 28), 'employee_id': 2},
    {'total_work_hours': 159.00, 'salary': 6000.00, 'net_salary': 5400.00, 'payment_date': date(2024, 7, 28), 'employee_id': 3},
    {'total_work_hours': 157.75, 'salary': 4800.00, 'net_salary': 4320.00, 'payment_date': date(2024, 7, 28), 'employee_id': 4},
    {'total_work_hours': 159.50, 'salary': 5200.00, 'net_salary': 4680.00, 'payment_date': date(2024, 7, 28), 'employee_id': 5},
    {'total_work_hours': 158.75, 'salary': 5700.00, 'net_salary': 5130.00, 'payment_date': date(2024, 7, 28), 'employee_id': 6},

    # June 2024 payroll
    {'total_work_hours': 157.00, 'salary': 5000.00, 'net_salary': 4500.00, 'payment_date': date(2024, 6, 28), 'employee_id': 1},
    {'total_work_hours': 157.50, 'salary': 5500.00, 'net_salary': 4950.00, 'payment_date': date(2024, 6, 28), 'employee_id': 2},
    {'total_work_hours': 156.00, 'salary': 6000.00, 'net_salary': 5400.00, 'payment_date': date(2024, 6, 28), 'employee_id': 3},
    {'total_work_hours': 157.25, 'salary': 4800.00, 'net_salary': 4320.00, 'payment_date': date(2024, 6, 28), 'employee_id': 4},
    {'total_work_hours': 158.00, 'salary': 5200.00, 'net_salary': 4680.00, 'payment_date': date(2024, 6, 28), 'employee_id': 5},
    {'total_work_hours': 159.00, 'salary': 5700.00, 'net_salary': 5130.00, 'payment_date': date(2024, 6, 28), 'employee_id': 6},
]


# Loop through each payroll record and add it to the storage
for payroll in payroll_data:
    payroll_record = Payroll(**payroll)
    storage.new(payroll_record)


catagory_data = [
    {'catagory_name': 'Charger'},
    {'catagory_name': 'Adapter'},
    {'catagory_name': 'Light'},
]

# Example of how you might insert these into the database:
for data in catagory_data:
    catagory = Catagory(**data)
    storage.new(catagory)  # Assuming `storage` is your session manager

from datetime import datetime
from models import storage
from models.product import Product

# Sample product data with varying types and categories
product_data = [
    {'product_name': 'Fast Charger 20W', 'product_type': 'st11', 'quantity': 100, 'price': 19.99, 'production_date': datetime(2024, 8, 28), 'category_id': 1},
    {'product_name': 'Wireless Charger', 'product_type': 'st12', 'quantity': 150, 'price': 29.99, 'production_date': datetime(2024, 8, 28), 'category_id': 1},
    {'product_name': 'LED Light Bulb', 'product_type': 'st21', 'quantity': 200, 'price': 9.99, 'production_date': datetime(2024, 8, 28), 'category_id': 3},
    {'product_name': 'Smart Light Strip', 'product_type': 'st22', 'quantity': 120, 'price': 24.99, 'production_date': datetime(2024, 8, 28), 'category_id': 3},
    {'product_name': 'USB-C Adapter', 'product_type': 'st31', 'quantity': 180, 'price': 14.99, 'production_date': datetime(2024, 8, 28), 'category_id': 2},
    {'product_name': 'Multiport Adapter', 'product_type': 'st32', 'quantity': 130, 'price': 34.99, 'production_date': datetime(2024, 8, 28), 'category_id': 2},
    # More entries...
]

# Adding additional products for a larger dataset
for i in range(100):  # Simulating a large dataset
    product_data.append({
        'product_name': f'Product {i}',
        'product_type': f'st{i % 10 + 11}',  # Varying product type
        'quantity': 50 + i,
        'price': 9.99 + (i % 10),
        'production_date': datetime(2024, 8, 28),
        'category_id': (i % 3) + 1  # Alternating categories
    })

# Insert products into the database
for product in product_data:
    new_product = Product(**product)
    storage.new(new_product)

# Save the changes to the database
storage.save()

# Close the session
storage.close()
