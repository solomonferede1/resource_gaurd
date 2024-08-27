#!/usr/bin/python3
"""Employee model - create and manage the organization employee date """


from base_model import Base
from sqlalchemy import Column, String, Integer


class Employee(Base):
    '''Employee class - mapped with employee table'''

    __tablename__ = 'employee'

    id = Column(Integer, nullable=False, primary_key=True)