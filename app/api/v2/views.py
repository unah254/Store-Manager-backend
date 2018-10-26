# module imports
import datetime
from flask_restful import Resource, reqparse

from functools import wraps
from werkzeug.security import check_password_hash
from flask import Flask, request, jsonify

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# local imports
from .models import User, Users, ProductItem, Products
from .utils import Validators




def admin_only(_f):
    ''' Restrict access if not admin '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().fetch_by_email(get_jwt_identity())

        print(user)

        if not user.admin:
            return {'message': 'Anauthorized access, you must be an admin to access this level'}, 401
        return _f(*args, **kwargs)
    return wrapper_function

def user_only(_f):
    ''' Restrict access if not attendant '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().fetch_by_email(get_jwt_identity())

        if user.admin:
            return {'message': 'Anauthorized access, you must be an attendant to access this level'}, 401
        return _f(*args, **kwargs)
    return wrapper_function

class SignUp(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")
    

    @jwt_required
    @admin_only
    def post(self):
        """ Create a new user"""
        data = SignUp.parser.parse_args()

        email = data["email"]
        password = data["password"]
        

        validate = Validators()


        if not validate.valid_email(email):
            return {"message": "enter valid email"}, 400

        # if not validate.valid_password(password):
        #     return {"message": "password should start with a capital letter and include a number"}, 400


        if User().fetch_by_email(email):
            return {"message": "user with {} already exists".format(email)}, 400

        user = User(email, password)
        user.add()

        return {"message": "user {} created successfully".format(email)}, 201


class Login(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("email", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")

    def post(self):
        data = Login.parser.parse_args()

        email = data["email"]
        password = data["password"]

        user = User().fetch_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            expires = datetime.timedelta(days=2)
            token = create_access_token(user.email, expires_delta=expires)
            return {'token': token, 'message': 'successfully logged'}, 200
        return {'message': 'user not found'}, 404
    
class CreateProduct(Resource):
    '''to get input from user and create a new product'''
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                         help="This field cannot be left blank")
   

    parser.add_argument('price', type=int, required=True,
                        help="This field cannot be left blank")
    

    parser.add_argument('category', type=str, required=True,
                        help="This field cannot be left blank!")
    
    @jwt_required
    @admin_only
    def post(self):
        ''' add new product'''
        data = request.get_json()

        name = data['name']
        price = data['price']
        category = data['category']

        if not Validators().valid_product_name(name):
            return {'message': 'Enter valid product name'}, 400
        
        
        # product = ProductItem(name=name, category=category, price=price)
        product = ProductItem().fetch_by_name(name)
        if product:
            return {'message':'product already exists'}, 400
        
        product = ProductItem(name=name, category=category, price=price)

        product.add()

        return {"message": "product successfuly created", "product": product.serialize()}, 201


class AllProducts(Resource):

    def get(self):
        ''' get all products '''
        productitems = ProductItem().fetch_all_productitems()

        if not productitems:
            return {"message": "There are no productitems for now "}, 404

        return {"Product items": [productitem.serialize() for productitem in productitems]}, 200

        
class SingleProduct(Resource):
    '''class to get a specific product'''

    def get(self, id):
        ''' get a specific product '''

        product = ProductItem().fetch_by_id(id)

        if product:
            return {"Products": product.serialize()}

        return {'message': "Not found"}, 404
    @jwt_required
    @admin_only
    def delete(self, id):
        ''' Delete a single product '''

        product = ProductItem().fetch_by_id(id)
        if product:
           ProductItem().delete(id)
        return {'message': "Succesfully Deleted"}, 200
        
    @jwt_required
    @admin_only
    def put(self, product_id):
        """ Modify a product """
        data = request.get_json()

        name = data['name']
        price = data['price']
        category = data['category']
        product = ProductItem().fetch_by_id(product_id)

        if product:
            ProductItem().update(product_id, name, price, category)

        return {'message':'Succesfully modified'}, 200
        # if not product:
        #     return {'message':'no product to be modified'}, 
        # ProductItem().update(product_id)
        # return {'message':'product modified succesfully'}, 200