#!/usr/bin/python3
'''Raw materials Transaction records model'''

from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime

class RawMaterialTransaction(BaseModel, Base):
    '''RawMaterialTransaction model representing transactions on raw materials.'''

    __tablename__ = 'raw_material_transactions'

    transaction_type = Column(Enum('add', 'withdraw', name='transaction_type_enum'), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    transaction_by_employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    raw_material_id = Column(Integer, ForeignKey('raw_materials.id'), nullable=False)


    def __init__(self, *args, **kwargs):
        '''Initialize the raw material transaction with the given attributes.'''
        super().__init__(*args, **kwargs)
