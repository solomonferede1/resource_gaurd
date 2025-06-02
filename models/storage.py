#!/usr/bin/python3
'''DB storage'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
import os
from models.base_model import Base
from models.employee import Employee
from models.attendance import Attendance
from models.payroll import Payroll
from models.category import Category
from models.product import Product
from models.supplier import Supplier
from models.raw_material import RawMaterial
from models.product_transaction import ProductTransaction
from models.raw_material_transaction import RawMaterialTransaction


classes = {'Employee' : Employee, 'Attendance' : Attendance,
           'Payroll' : Payroll, 'Category' : Category,
           'Product' : Product, 'Supplier' : Supplier,
           'RawMaterial' : RawMaterial, 'ProductTransaction' : ProductTransaction,
           'RawMaterialTransaction' : RawMaterialTransaction}


class DBStorage:
    '''Database Storage class'''

    __engine = None
    __session = None

    def __init__(self):
        '''Initialization'''
        

        MYSQL_USER = os.environ.get('MYSQL_USER', 'RG_USER')
        MYSQL_PWD = os.environ.get('MYSQL_PWD', 'RG_PASSWORD')
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_DB = os.environ.get('MYSQL_DB', 'RG_DB')

        # Optional: other environment variables
        RG_API_HOST = os.environ.get('RG_API_HOST', '0.0.0.0')
        RG_API_PORT = os.environ.get('RG_API_PORT', '5000')
        RG_WEB_PORT = os.environ.get('RG_WEB_PORT', '5050')


        url = f'mysql+mysqldb://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}/{MYSQL_DB}'
        self.__engine = create_engine(url, echo=False)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        id = int(id) if isinstance(id, str) and id.isdigit() else id
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count

    def find_employee_by_email(self, email):
        """More efficient email lookup"""
        for emp in self.all(Employee).values():
            if emp.email == email:
                return emp
        return None

    def products_filter_by_category(self, category_id):
        """
        Returns a list of Product objects filtered by category_id.
        Converts each product to a dictionary before returning.
        
        Args:
            category_id: The category ID to filter by (int or str)
            
        Returns:
            List of product dictionaries
        """
        if not category_id:
            return []

        try:
            category_id = int(category_id)
            products = [
                product for product in self.all(Product).values()
                if product.category_id == category_id
            ]
            return [product.to_dict() for product in products]
        except (ValueError, TypeError):
            return []
