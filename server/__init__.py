# Caden Kriese - 03-17-2020
"""
Backend API for Student Solutions
"""

from dynaconf import FlaskDynaconf
from flask import Flask

import server.v1


def create_app():
    """
    Creates the Flask application.
    :return: The Flask application.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    FlaskDynaconf(app)
    v1.api.init_app(app)
    v1.register()

    return app
