#!/usr/bin/python3
'''Product transaction record model'''

from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime

class ProductTransaction(BaseModel, Base):
    '''ProductTransaction model representing transactions on products.'''

    __tablename__ = 'product_transactions'

    transaction_type = Column(Enum('add', 'withdraw', name='transaction_type_enum'), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    transaction_by_employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)


    def __init__(self, *args, **kwargs):
        '''Initialize the product transaction with the given attributes.'''
        super().__init__(*args, **kwargs)
