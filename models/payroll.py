#!/usr/bin/python3
'''The Payroll model - Database'''

from models.employee import Employee
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey, Computed
from sqlalchemy.orm import relationship
from datetime import datetime


class Payroll(BaseModel, Base):
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

    total_work_hours = Column(Numeric(6, 2), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    net_salary = Column(Numeric(10, 2), Computed('salary * 0.75', persisted=True))
    payment_date = Column(Date, default=datetime.now, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)


    def __init__(self, *args, **kwargs):
        '''Create from kwargs'''
        super().__init__(*args, **kwargs)
