# Caden Kriese - 04-10-2020
"""
API Version 1.0
"""

from flask import Blueprint
from flask_restx import Api

from server.v1.infinite_campus import ns as infinite_campus
from server.v1.models import *

v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1, title='Student Solutions',
          description='An API for the backend operations of Student Solutions.',
          version='1.0')

api.add_namespace(infinite_campus)

# Add models for Swagger.
api.add_model('course', course)
api.add_model('grade_section', grade_section)
api.add_model('grade_category', grade_category)
api.add_model('assignment', assignment)
