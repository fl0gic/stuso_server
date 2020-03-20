# Caden Kriese - 03-17-2020
from flask import Blueprint
from flask_restful import Api

from server.infinite_campus.classbook_api import ClassbooksAPI

infinite_campus = Blueprint('infinite_campus', __name__, url_prefix='/ic')
api = Api(infinite_campus)


def create_routes(app):
    app.register_blueprint(infinite_campus)
    api.add_resource(ClassbooksAPI, '/classbooks')
