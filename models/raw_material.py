#!?usr/bin/python3
'''Raw materials table'''

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from datetime import datetime

class RawMaterial(BaseModel, Base):
    '''RawMaterial model class representing raw materials in the inventory.'''
    
    __tablename__ = 'raw_materials'
    
    material_name = Column(String(60), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)

    # Define the relationship to the Supplier
    supplier = relationship('Supplier', backref='raw_materials')

    def __init__(self, *args, **kwargs):
        '''Initialize the raw material with the given attributes.'''
        super().__init__(*args, **kwargs)
