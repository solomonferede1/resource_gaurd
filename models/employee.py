#!/usr/bin/python3
"""Employee model - create and manage the organization employee date """


from datetime import datetime
from flask_login import UserMixin
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.orm import relationship, backref


class Employee(BaseModel, Base, UserMixin):
    '''Employee class - mapped with employee table'''

    __tablename__ = 'employees'

    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(200), nullable=False)
    gender = Column(String(60), nullable=True)
    status = Column(String(60), nullable=True, default='active')
    role = Column(String(60), default='employee')
    department = Column(String(60), default='Production')
    email = Column(String(60), unique=True, nullable=True)
    phone = Column(String(60), unique=True, nullable=False)
    salary = Column(Numeric(10, 2))
    date_hired = Column(DateTime, default=datetime.utcnow)

    # Define relationships
    attendances = relationship("Attendance",
                              backref="employee",
                              cascade="all, delete, delete-orphan")

    payrolls = relationship("Payroll",
                              backref="employee",
                              cascade="all, delete, delete-orphan")

    product_transactions = relationship('ProductTransaction',
                                        backref=backref('employee', passive_deletes=True),
                                        cascade="save-update, merge")

    raw_material_transactions = relationship('RawMaterialTransaction',
                                             backref=backref('employee', passive_deletes=True),
                                             cascade="save-update, merge")


    @property
    def is_active(self):
        """Required for Flask-Login"""
        return self.status == 'active'


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)