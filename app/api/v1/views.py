import datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# imported module to validate the inputs
from .utils import Validators
from .models import Product, Salesrecord, User, Users, products

def admin_only(_f):
    ''' Restrict access if not admin '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().get_by_email(get_jwt_identity())

        print(user)

        if not user.admin:
            return {'message': 'Anauthorized access, you must be an admin to access this level'}, 401
        return _f(*args, **kwargs)
    return wrapper_function

def user_only(_f):
    ''' Restrict access if not attendant '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().get_by_email(get_jwt_identity())

        if user.admin:
            return {'message': 'Anauthorized access, you must be an attendant to access this level'}, 401
        return _f(*args, **kwargs)
    return wrapper_function



class Createproduct(Resource):
    '''to get input from user and create a new product'''
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                         help="This field cannot be left blank")
   

    parser.add_argument(
        'price',
        type=int,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument(
        'category',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
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
        # if not Validators().valid_product_description(description):
        #     return {'message': 'Enter valid product description'}, 400
        
        product = Product(name, price, category)

        products.append(product)

        return {"message": "product added"}, 201


class Allproducts(Resource):

    def get(self):
        ''' get all products '''

        return {'Allproducts': [product.serialize() for product in products]}, 200


class Singleproduct(Resource):
    '''class to get a specific product'''

    def get(self, id):
        ''' get a specific order '''

        product = Product().get_id(id)

        if product:
            return {"Products": product.serialize()}

        return {'message': "Not found"}, 404
    @jwt_required
    @admin_only
    def delete(self, id):
        ''' Delete a single product '''

        product = Product().get_id(id)
        if product:
            products.remove(product)
            return {'message': "Deleted"}, 200
        return {'message': "Not found"}, 404


sales=[]
class Createrecord(Resource):
    '''to get input from user and create a new record'''
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument("price", type=float, required=True,
                        help="This field cannot be left blank")
    

    parser.add_argument("quantitysold", type=int, required=True,
                         help="This field cannot be left blank!")

    parser.add_argument("amountbrought", type=int, required=True,
                         help="This field cannot be left blank!")
    
    @jwt_required
    @user_only
    def post(self):
        ''' add new record'''
        data = Createrecord.parser.parse_args()
        data = request.get_json()

        name = data['name']
        price= data['price']
        quantitysold = data['quantitysold']
        amountbrought = data['amountbrought']

        if not Validators().valid_product_name(name):
            return {'message': 'Enter valid product name'}, 400

        sale = Salesrecord(name, price, quantitysold, amountbrought)

        sales.append(sale)

        return {"message": "record created"}, 201


class Allsales(Resource):

    def get(self):
        ''' get all salerecords '''

        return {'Allsales': [sale.serialize() for sale in sales]}, 200


class Singlesale(Resource):
    '''class to get a specific record'''

    def get(self, id):
        ''' get a specific record '''

        sale = Salesrecord().get_by_id(id)

        if sale:
            return {"Salesrecord": sale.serialize()}

        return {'message': "Not found"}, 404
    @jwt_required
    @admin_only
    def delete(self, id):
        ''' Delete a single record '''

        record = Salesrecord().get_by_id(id)
        if record:
            sales.remove(record)
            return {'message': "Deleted"}, 200
        return {'message': "Not found"}, 404

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

        if not validate.valid_password(password):
            return {"message": "password should start with a capital letter and include a number"}, 400


        if User().get_by_email(email):
            return {"message": "user with {} already exists".format(email)}, 400

        user = User(email, password)
        Users.append(user)

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

        user = User().get_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            expires = datetime.timedelta(days=2)
            token = create_access_token(user.email, expires_delta=expires)
            return {'token': token, 'message': 'successfully logged'}, 200
        return {'message': 'user not found'}, 404
    
