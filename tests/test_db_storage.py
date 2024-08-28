import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.employee import Employee
from models.attendance import Attendance
from models.payroll import Payroll
from models.storage import DBStorage

class TestDBStorage(unittest.TestCase):
    '''Test the DB storage class and thier methods'''

    def test_employee_creation(self):
        """Test the creation of an Employee object"""
        employee = Employee(first_name="John", last_name="Doe",
                            email="john.doe@example.com",
                            phone="1234567890", salary=5000)
        self.storage.new(employee)
        self.storage.save()

        # Verify the employee was added to the database
        all_employees = self.session.query(Employee).all()
        self.assertEqual(len(all_employees), 1)
        self.assertEqual(all_employees[0].first_name, "John")
        self.assertEqual(all_employees[0].last_name, "Doe")
        self.assertEqual(all_employees[0].email, "john.doe@example.com")

    def test_attendance_creation(self):
        """Test the creation of an Attendance object"""
        # Assume an employee exists
        employee = Employee(first_name="John", last_name="Doe",
                            email="john.doe@example.com",
                            phone="1234567890", salary=5000)
        self.storage.new(employee)
        self.storage.save()

        # Create attendance
        attendance = Attendance(employee_id=employee.id, status=True)
        self.storage.new(attendance)
        self.storage.save()

        # Verify the attendance was added to the database
        all_attendances = self.session.query(Attendance).all()
        self.assertEqual(len(all_attendances), 1)
        self.assertEqual(all_attendances[0].employee_id, employee.id)
        self.assertTrue(all_attendances[0].status)

    def test_payroll_creation(self):
        """Test the creation of a Payroll object"""
        # Assume an employee exists
        employee = Employee(first_name="John", last_name="Doe",
                            email="john.doe@example.com", phone="1234567890", salary=5000)
        self.storage.new(employee)
        self.storage.save()

        # Create payroll
        payroll = Payroll(employee_id=employee.id, total_work_hours=160, salary=5000, net_salary=4500, payment_date='2024-08-01')
        self.storage.new(payroll)
        self.storage.save()

        # Verify the payroll was added to the database
        all_payrolls = self.session.query(Payroll).all()
        self.assertEqual(len(all_payrolls), 1)
        self.assertEqual(all_payrolls[0].employee_id, employee.id)
        self.assertEqual(all_payrolls[0].total_work_hours, 160)
        self.assertEqual(all_payrolls[0].salary, 5000)
        self.assertEqual(all_payrolls[0].net_salary, 4500)

    def test_storage_all(self):
        """Test the all method of DBStorage"""
        # Create employees
        employee1 = Employee(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", salary=5000)
        employee2 = Employee(first_name="Jane", last_name="Doe", email="jane.doe@example.com", phone="0987654321", salary=6000)
        self.storage.new(employee1)
        self.storage.new(employee2)
        self.storage.save()

        # Verify all employees are retrieved
        all_employees = self.storage.all(Employee)
        self.assertEqual(len(all_employees), 2)

    def test_storage_get(self):
        """Test the get method of DBStorage"""
        # Create an employee
        employee = Employee(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", salary=5000)
        self.storage.new(employee)
        self.storage.save()

        # Get the employee by ID
        found_employee = self.storage.get(Employee, employee.id)
        self.assertIsNotNone(found_employee)
        self.assertEqual(found_employee.id, employee.id)
        self.assertEqual(found_employee.first_name, "John")

    def test_storage_count(self):
        """Test the count method of DBStorage"""
        # Create employees
        employee1 = Employee(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", salary=5000)
        employee2 = Employee(first_name="Jane", last_name="Doe", email="jane.doe@example.com", phone="0987654321", salary=6000)
        self.storage.new(employee1)
        self.storage.new(employee2)
        self.storage.save()

        # Verify the count of all employees
        count = self.storage.count(Employee)
        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()
