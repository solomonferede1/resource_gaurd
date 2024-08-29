#!/usr/bin/python3
'''The supplier model'''

from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Supplier(BaseModel, Base):
    '''Supplier model class representing suppliers.'''
    
    __tablename__ = 'suppliers'
    
    name = Column(String(60), nullable=False)
    contact_info = Column(String(60), nullable=True)
    email = Column(String(60), nullable=True)
    address = Column(String(200), nullable=True)

    # Define the relationship to the raw materials they supply
    raw_materials = relationship('RawMaterial', backref='supplier',
                                 cascade='all, delete, delete-orphan')

    def __init__(self, *args, **kwargs):
        '''Initialize the supplier with the given attributes.'''
        super().__init__(*args, **kwargs)