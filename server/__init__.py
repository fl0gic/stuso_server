# Caden Kriese - 03-17-2020
"""
Backend API for Student Solutions
"""

from dynaconf import FlaskDynaconf
from flask import Flask

from server.v1 import v1


def create_app():
    """
    Creates the Flask application.
    :return: The Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    FlaskDynaconf(app)
    app.register_blueprint(v1)

    return app
