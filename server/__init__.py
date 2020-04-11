# Caden Kriese - 03-17-2020
"""
Backend API for Student Solutions
"""

from dynaconf import FlaskDynaconf
from flask import Flask

import server.v1.infinite_campus
from server.v1 import api


def create_app():
    """
    Creates the Flask application.
    :return: The Flask application.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    FlaskDynaconf(app)
    api.init_app(app)

    return app
