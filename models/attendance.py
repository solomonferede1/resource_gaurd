#!/usr/bin/python3
'''Attendance database - model'''


from datetime import date, datetime
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, Numeric,\
    Boolean, ForeignKey, DateTime, Date, Computed
from sqlalchemy.orm import relationship

class Attendance(BaseModel, Base):
    '''Attendance'''

    __tablename__ = 'attendances'

    attendance_date = Column(Date, default=date.today)
    check_in_time = Column(DateTime, default=datetime.now())
    check_out_time = Column(DateTime, default=datetime.now())
    total_work_hours = Column(Numeric(4, 2),
                              Computed("TIMESTAMPDIFF(Hour,\
                                       check_in_time, check_out_time)",
                                       persisted=True))
    status = Column(Boolean)

    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
