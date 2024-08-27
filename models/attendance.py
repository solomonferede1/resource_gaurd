#!/usr/bin/python3
'''Attendance database - model'''


from models.employee import Employee
from base_model import Base
from sqlalchemy import Column, Integer, String, Numeric,\
    Boolean, ForeignKey, DateTime, Date, Computed
from sqlalchemy.orm import Relationship
from datetime import date

class Attendance(Base):
    '''Attendance'''

    __tablename__ = 'attendances'

    id = Column(Integer, primary_key=True)
    attendance_date = Column(Date, default=date.today)
    check_in_time = Column(DateTime, nullable=True)
    check_out_time = Column(DateTime, nullable=True)
    total_work_hours = Column(Numeric(4, 2),
                              Computed("TIMESTAMPDIFF(Hour,\
                                       check_in_time, check_out_time)",
                                       persisted=True))
    status = Column(Boolean)

    employee_id = Column(Integer, ForeignKey('Employee.id', ondelete='CASCADE'), nullable=False)
    employee = Relationship('Employee', back_populates='attendances')


Employee.attendances = Relationship('Attendance', back_populates='employee')
