#!/usr/bin/python3
"""Views module"""

from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.employee import *
from api.v1.views.attendance import *
from api.v1.views.payroll import *
from api.v1.views.product import *
from api.v1.views.raw_materials import *