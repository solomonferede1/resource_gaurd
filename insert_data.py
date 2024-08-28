#!/usr/bin/python3

from models import storage
from models.employee import Employee
from models.attendance import Attendance

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
    storage.save() 

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

# Commit the transaction
storage.save()

# Close the session
storage.close()
