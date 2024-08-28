#!/usr/bin/python3
'''Catagory model'''


from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Catagory(BaseModel, Base):
    '''Define the catagory'''

    __tablename__ = 'catagories'

    catagory_name = Column(String(60), nullable=False)

    products = relationship('Product', backref='catagory',
                            cascade='all, delete, delete-orphan')

    def __init__(self, *args, **kwargs):
        '''Initialise the remaining att'''
        super().__init__(*args, **kwargs)
