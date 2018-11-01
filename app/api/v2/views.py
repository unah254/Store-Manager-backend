# module imports
import datetime
from functools import wraps
from flask_restful import Resource, reqparse


from werkzeug.security import check_password_hash
from flask import request, make_response

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
# local imports
from .models import User, ProductItem, SalesRecord
from .utils import Validators

blacklist=set()
def admin_only(_f):
    ''' Restrict access if not admin '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().fetch_by_email(get_jwt_identity())

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

        # validate = Validators()

        # if not validate.valid_email(email):
        #     return {"message": "enter valid email"}, 400

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

class Logout(Resource):
    @jwt_required
    def post(self):
        try:
            jti=get_raw_jwt()['jti']
            blacklist.add(jti)
            return {'message':'successfuly logged out'}, 200
        except:
            return {'message': 'set authorization'}, 404



class CreateProduct(Resource):
    '''to get input from user and create a new product'''
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('price', type=int, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('category', type=str, required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('quantity', type=int, required=True,
                        help="This field cannot be left blank!")

    @jwt_required
    @admin_only
    def post(self):
        ''' add new product'''
        data = request.get_json(force=True)

        name = data['name']
        price = data['price']
        category = data['category']
        quantity = data['quantity']

        if not Validators().valid_product_name(name):
            return {'message': 'Enter valid product name'}, 400

        # product = ProductItem(name=name, category=category, price=price)
        product = ProductItem().fetch_by_name(name)
        if product:
            return {'message': 'product already exists, please update product'}, 400

        product = ProductItem(name=name, category=category,
                              price=price, quantity=quantity)

        product.add()

        return {"message": "product successfuly created", "product": product.serialize()}, 201


class AllProducts(Resource):
    @jwt_required
    @admin_only
    def get(self):
        ''' get all products '''
        productitems = ProductItem().fetch_all_productitems()

        if not productitems:
            return {"message": "There are no productitems for now "}, 404
        all_pros = []
        for p in productitems:
            format_p = {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "quantity": p.quantity
            }
            all_pros.append(format_p)

        return {"message": "success", "Product items": all_pros}, 200


class SingleProduct(Resource):
    '''class to get a specific product'''
    @jwt_required
    @admin_only
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

        if not product:
            return {"message": "There are no productitems for now "}, 404

    @jwt_required
    @admin_only
    def put(self, id):
        """ Modify a product """
        data = request.get_json()

        name = data['name']
        price = data['price']
        category = data['category']
        quantity = data['quantity']
        product = ProductItem().fetch_by_id(id)

        if product:
            ProductItem().update(id, name, price, category, quantity)

        return {'message': 'product succesfully modified'}, 200
        # if not product:
        #     return {'message':'no product to be modified'},
        # ProductItem().update(product_id)
        # return {'message':'product modified succesfully'}, 200


class AddSaleRecord(Resource):
    '''to get input from user and create a new record'''
    parser = reqparse.RequestParser()
    parser.add_argument('creator_name', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('product_id', type=int, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('price', type=int, required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('quantity_to_sell', type=int, required=True,
                        help="This field cannot be left blank!")
   
    @jwt_required
    @user_only
    def post(self):
        ''' add new sale record'''
        data = request.get_json()

        creator_name = data['creator_name']
        product_id = int(data['product_id'])
        quantity_to_sell = int(data['quantity_to_sell'])

        # if not Validators().valid_product_name(name):
        #     return {'message': 'Enter valid product name'}, 400

        record = SalesRecord().fetch_by_id(product_id)
        if not record:
            return {'message': 'product does not exist'}, 400

        sales = SalesRecord(
            product_id=product_id, creator_name=creator_name, quantity_to_sell=quantity_to_sell)

        sales.create_sales(product_id, quantity_to_sell, creator_name)

        return {"message": "record successfuly created", "salesrecord": sales.serialize()}, 201


class RecordsCreated(Resource):
    @jwt_required
    @user_only
    def get(self):
        ''' get all sale records '''
        records = SalesRecord().fetch_all_salesrecords()

        if not records:
            return {"message": "No records available "}, 404
