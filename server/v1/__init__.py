# Caden Kriese - 4/13/20
"""
    API Version 1.0
"""
from flask_smorest import Api

from server.v1.infinitecampus import bp as infinite_campus

api = Api(prefix='test')


def register():
    """
        Registers the blueprints from all modules.
    """
    api.register_blueprint(infinite_campus)
