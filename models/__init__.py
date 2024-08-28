#!/usr/bin/python3
"""
initialize the models package
"""


from models.storage import DBStorage


storage = DBStorage()
storage.reload()