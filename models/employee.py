#!/usr/bin/python3
"""Employee model - create and manage the organization employee date """


from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.orm import relationship 


class Employee(BaseModel, Base):
    '''Employee class - mapped with employee table'''

    __tablename__ = 'employees'

    first_name = Column(String(60))
    last_name = Column(String(60))
    role = Column(String(60))
    email = Column(String(60), unique=True, nullable=True)
    phone = Column(String(60), unique=True, nullable=False)
    salary = Column(Numeric(10, 2))
    date_hired = Column(DateTime, default=datetime.utcnow())

    attendances = relationship("Attendance",
                              backref="employee",
                              cascade="all, delete, delete-orphan")

    payroll = relationship("Payroll",
                              backref="employee",
                              cascade="all, delete, delete-orphan")


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)