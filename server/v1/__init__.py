# Caden Kriese - 04-10-2020
from flask import Blueprint
from flask_restplus import Api

from server.v1 import infinite_campus

api = Api(title='Student Solutions',
          description='An API for the backend operations of Student Solutions.',
          version='1.0')
v1 = Blueprint('v1', __name__, url_prefix='/api/v1')

api.register_blueprint(v1)
