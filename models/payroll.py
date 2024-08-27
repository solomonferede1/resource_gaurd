#!/usr/bin/python3
'''The Payroll model - Database'''

from models.employee import Employee
from base_model import Base
from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey, Index
from sqlalchemy.orm import relationship


class Payroll(Base):
    '''
    Payroll model class representing employee payroll records.

    Attributes:
    - id: Primary key - an auto-incrementing integer.
    - total_work_hours: The total number of work hours for the month
    - salary: The total salary for the month i.e Gross Salary.
    - net_salary: The net salary after deductions/tax.
    - payment_date: The date when the payment was made.
    - employee_id: Foreign key linking payroll record to an employee.
    - employee: Relationship to the Employee model
    (used to establish many-to-one relationship between Payroll and Employee).
    '''

    __tablename__ = 'payrolls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_work_hours = Column(Numeric(6, 2), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    net_salary = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)

    # Relationship to the Employee model
    employee = relationship('Employee', back_populates='payrolls')


Employee.payrolls = relationship('Payroll', back_populates='employee')
