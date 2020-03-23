# Caden Kriese - 03-17-2020
"""
Infinite Campus module of Student Solutions backend API.
"""

from flask import Blueprint
from flask_restful import Api

from server.infinite_campus.courses import CoursesAPI

INFINITE_CAMPUS = Blueprint('infinite_campus', __name__, url_prefix='/ic/v1')
API = Api(INFINITE_CAMPUS)


def create_routes(app):
    """
    Defines the routes for the Infinite Campus module of the API.
    :param app: The flask app these routes will be added to.
    """
    app.register_blueprint(INFINITE_CAMPUS)
    API.add_resource(CoursesAPI, '/courses')
