#!/usr/bin/python3

from models import storage
from models.employee import Employee
from models.attendance import Attendance
from models.payroll import Payroll
from models.catagory import Catagory
from models.product import Product
from models.supplier import Supplier
from models.raw_material import RawMaterial
from models.product_transaction import ProductTransaction
from models.raw_material_transaction import RawMaterialTransaction
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


suppliers_data = [
    {'name': 'ABC Electronics', 'contact_info': '0123456789', 'email': 'abc@electronics.com', 'address': '123 Main Street, City, Country'},
    {'name': 'XYZ Components', 'contact_info': '0987654321', 'email': 'xyz@components.com', 'address': '456 Market Road, City, Country'},
    {'name': 'LMN Industrial', 'contact_info': '1112223334', 'email': 'lmn@industrial.com', 'address': '789 Factory Avenue, City, Country'}
]

# Insert suppliers into the database
for supplier_data in suppliers_data:
    supplier = Supplier(**supplier_data)
    storage.new(supplier)


raw_materials_data = [
    {'material_name': 'Copper Wire', 'quantity': 5000, 'unit_price': 10.50, 'created_at': datetime(2024, 8, 1), 'updated_at': datetime(2024, 8, 1), 'supplier_id': 1},
    {'material_name': 'Plastic Casing', 'quantity': 3000, 'unit_price': 5.75, 'created_at': datetime(2024, 8, 2), 'updated_at': datetime(2024, 8, 2), 'supplier_id': 2},
    {'material_name': 'Circuit Board', 'quantity': 2000, 'unit_price': 25.00, 'created_at': datetime(2024, 8, 3), 'updated_at': datetime(2024, 8, 3), 'supplier_id': 3},
    {'material_name': 'LED Light', 'quantity': 4000, 'unit_price': 3.40, 'created_at': datetime(2024, 8, 4), 'updated_at': datetime(2024, 8, 4), 'supplier_id': 1},
    {'material_name': 'Resistor', 'quantity': 10000, 'unit_price': 0.10, 'created_at': datetime(2024, 8, 5), 'updated_at': datetime(2024, 8, 5), 'supplier_id': 2},
    {'material_name': 'Capacitor', 'quantity': 8000, 'unit_price': 0.25, 'created_at': datetime(2024, 8, 6), 'updated_at': datetime(2024, 8, 6), 'supplier_id': 3},
]

# Insert raw materials into the database
for raw_material_data in raw_materials_data:
    raw_material = RawMaterial(**raw_material_data)
    storage.new(raw_material)



# Example data for product transactions
product_transactions_data = [
    {'transaction_type': 'add', 'quantity': 100, 'transaction_date': datetime(2024, 8, 1, 9, 0), 'transaction_by_employee_id': 1, 'product_id': 1},
    {'transaction_type': 'withdraw', 'quantity': 50, 'transaction_date': datetime(2024, 8, 3, 10, 30), 'transaction_by_employee_id': 2, 'product_id': 2},
    {'transaction_type': 'add', 'quantity': 200, 'transaction_date': datetime(2024, 8, 5, 11, 15), 'transaction_by_employee_id': 3, 'product_id': 3},
    {'transaction_type': 'withdraw', 'quantity': 70, 'transaction_date': datetime(2024, 8, 7, 14, 45), 'transaction_by_employee_id': 4, 'product_id': 4},
    {'transaction_type': 'add', 'quantity': 150, 'transaction_date': datetime(2024, 8, 10, 8, 20), 'transaction_by_employee_id': 5, 'product_id': 5},
    {'transaction_type': 'withdraw', 'quantity': 30, 'transaction_date': datetime(2024, 8, 12, 16, 50), 'transaction_by_employee_id': 6, 'product_id': 6},
]

# Insert the data
for data in product_transactions_data:
    transaction = ProductTransaction(**data)
    storage.new(transaction)
    storage.save()

# Example data for raw material transactions
raw_material_transactions_data = [
    {'transaction_type': 'add', 'quantity': 500, 'transaction_date': datetime(2024, 8, 2, 9, 0), 'transaction_by_employee_id': 1, 'raw_material_id': 1},
    {'transaction_type': 'withdraw', 'quantity': 200, 'transaction_date': datetime(2024, 8, 4, 10, 30), 'transaction_by_employee_id': 2, 'raw_material_id': 2},
    {'transaction_type': 'add', 'quantity': 300, 'transaction_date': datetime(2024, 8, 6, 11, 15), 'transaction_by_employee_id': 3, 'raw_material_id': 3},
    {'transaction_type': 'withdraw', 'quantity': 150, 'transaction_date': datetime(2024, 8, 8, 14, 45), 'transaction_by_employee_id': 4, 'raw_material_id': 4},
    {'transaction_type': 'add', 'quantity': 400, 'transaction_date': datetime(2024, 8, 11, 8, 20), 'transaction_by_employee_id': 5, 'raw_material_id': 5},
    {'transaction_type': 'withdraw', 'quantity': 100, 'transaction_date': datetime(2024, 8, 13, 16, 50), 'transaction_by_employee_id': 6, 'raw_material_id': 6},
]

# Insert the data
for data in raw_material_transactions_data:
    transaction = RawMaterialTransaction(**data)
    storage.new(transaction)
    storage.save()


# Save the changes to the database
storage.save()

# Close the session
storage.close()
