#!/usr/bin/python3
'''Products table/model'''

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Numeric, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Product(BaseModel, Base):
    '''Product model class representing products in the inventory.'''

    __tablename__ = 'products'

    product_name = Column(String(60), nullable=False)
    product_type = Column(String(60), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    production_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete column

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Define relationship
    transactions = relationship('ProductTransaction', backref='product')

    def __init__(self, *args, **kwargs):
        '''Call super basemodel class to initialize common att'''
        super().__init__(*args, **kwargs)
