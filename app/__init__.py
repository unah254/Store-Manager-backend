# imported necessary modules to create flask microframework
from flask import Flask
from flask_restful import  Api
from instance.config import app_config

from .api.v1.views import Createproduct, Allproducts, Singleproduct, Createrecord, Allsales, Singlesale


def create_app(config_name):
    """
    Given a configuration name, loads the correct 
    configuration from the config.py
    :param config_name: The configuration name to load the configuration
    :return: The app to be initialized
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    

    api = Api(app)
    api.add_resource(Createproduct, '/api/v1/products')
    api.add_resource(Allproducts, '/api/v1/products')
    api.add_resource(Singleproduct, '/api/v1/products/<int:id>')
    api.add_resource(Createrecord, '/api/v1/sales')
    api.add_resource(Allsales, '/api/v1/sales')
    api.add_resource(Singlesale, '/api/v1/sales/<int:id>')



        

    
    
    return app