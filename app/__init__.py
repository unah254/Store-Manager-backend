# imported necessary modules to create flask microframework
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager 
from flask_cors import CORS
from instance.config import app_config




# from .api.v2.views import User, ProductItem, SalesRecord
# from app.api.v2.views import User, ProductItem,SalesRecord

JWT = JWTManager()


def create_app(config_name):
    """
    Given a configuration name, loads the correct
    configuration from the config.py
    :param config_name: The configuration name to load the configuration
    :return: The app to be initialized
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    # app.config.from_object(app_config[config_name])s
    app.config.from_pyfile('config.py')
    app.config["JWT_SECRET_KEY"]=os.getenv("SECRET_KEY")
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
    with app.app_context():
        from .api.v2.views import (Login, SignUp, CreateProduct, AllProducts, SingleProduct, 
                                  AddSaleRecord, RecordsCreated, Logout, blacklist, Oneuser)
                                
    JWT.init_app(app)

    @JWT.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist



    api = Api(app)
    api.add_resource(Login, '/api/v2/login')
    api.add_resource(SignUp, '/api/v2/signup')
    api.add_resource(CreateProduct, '/api/v2/product')
    api.add_resource(AllProducts, '/api/v2/products')
    api.add_resource(SingleProduct, '/api/v2/products/<int:id>')
    api.add_resource(AddSaleRecord, '/api/v2/sales')
    api.add_resource(RecordsCreated, '/api/v2/sales')
    api.add_resource(Logout, '/api/v2/logout')
    api.add_resource(Oneuser, '/api/v2/user/<int:id>')



    return app
