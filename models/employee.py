#!/usr/bin/python3
"""Employee model - create and manage the organization employee date """


from base_model import Base
from sqlalchemy import Column, String, Integer, Numeric, DateTime


class Employee(Base):
    '''Employee class - mapped with employee table'''

    __tablename__ = 'employees'

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String(60))
    last_name = Column(String(60))
    role = Column(String(60))
    email = Column(String(60), unique=True, nullable=True)
    phone = Column(String(60), unique=True, nullable=False)
    salary = Column(Numeric(10, 2))
    date_hired = Column(DateTime)
