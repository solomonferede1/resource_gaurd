#!/usr/bin/python3
"""Employee model - create and manage the organization employee date """


from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric, DateTime


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


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)