# imported necessary modules to create flask microframework
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from instance.config import app_config


from .api.v2.views import Login, SignUp
from .api.v2.views import User, Users

JWT = JWTManager()


def create_app(config_name):
    """
    Given a configuration name, loads the correct 
    configuration from the config.py
    :param config_name: The configuration name to load the configuration
    :return: The app to be initialized
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    JWT.init_app(app)

    

    api = Api(app)
    api.add_resource(Login, '/api/v2/login')
    api.add_resource(SignUp, '/api/v2/signup')

    return app
