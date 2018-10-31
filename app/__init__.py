# imported necessary modules to create flask microframework
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from instance.config import app_config


from .api.v2.views import Login, SignUp, CreateProduct, AllProducts, SingleProduct, AddSaleRecord, RecordsCreated
from .api.v2.views import User, ProductItem, SalesRecord

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
    app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY")



    JWT.init_app(app)



    api = Api(app)
    api.add_resource(Login, '/api/v2/login')
    api.add_resource(SignUp, '/api/v2/signup')
    api.add_resource(CreateProduct, '/api/v2/product')
    api.add_resource(AllProducts, '/api/v2/products')
    api.add_resource(SingleProduct, '/api/v2/products/<int:id>')
    api.add_resource(AddSaleRecord, '/api/v2/sales')
    api.add_resource(RecordsCreated, '/api/v2/sales')

    return app
