from flask import Flask
from flask_restful import Resource, Api, reqparse
# imported module to validate the inputs
from .utils import Validators

# list to store products
products = []


class Product:
    '''product class to initialize products and display in json'''
    def __init__(self, name=None, price=None, description=None, category=None):
        '''create an instance of a new product'''
        self.id = len(products)+1
        self.name = name
        self.price = price
        self.description = description
        self.category = category

    def serialize(self):
        '''to get created data and display in json format'''
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            description=self.description,
            category=self.category
        )

    def get_id(self, product_id):
        '''display specific product id'''
        for product in products:
            if product.id == product_id:
                return product

class Createproduct(Resource):
    '''to get input from user and create a new product'''
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument(
        'description',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    parser.add_argument(
        'price',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument(
        'category',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        ''' add new product'''
        data = Createproduct.parser.parse_args()

        name = data['name']
        description = data['description']
        price = data['price']
        category = data['category']

        if not Validators().valid_product_name(name):
            return {'message': 'Enter valid product name'}, 400
        if not Validators().valid_product_description(description):
            return {'message': 'Enter valid product description'}, 400

        product = Product(name, price, description, category)

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

    def delete(self, id):
        ''' Delete a single product '''

        product = Product().get_id(id)
        if product:
            products.remove(product)
            return {'message': "Deleted"}, 200
        return {'message': "Not found"}, 404

sales=[]
class Salesrecord:
    '''sales class to initialize records and display in json'''
    def __init__(self, name=None, price=None,category=None, quantitysold=None, amountbrought=None):
        '''create an instance of a new sale record'''
        self.id = len(sales)+1
        self.name = name
        self.price = price
        self.quantitysold = quantitysold
        self.category = category
        self.amountbrought = amountbrought

    def serialize(self):
        '''to get created data and display in json format'''
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            quantitysold=self.quantitysold,
            category=self.category,
            amountbrought=self.amountbrought
        )

    def get_id(self, sales_id):
        '''display specific sales id'''
        for Salesrecord in sales:
            if Salesrecord.id == sales_id:
                return Salesrecord


class Createrecord(Resource):
    '''to get input from user and create a new record'''
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

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

    parser.add_argument(
        'quantitysold',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument(
        'amountbrought',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        ''' add new record'''
        data = Createrecord.parser.parse_args()

        name = data['name']
        price = data['price']
        category = data['category']
        quantitysold = data['quantitysold']
        amountbrought = data['amountbrought']

        if not Validators().valid_product_name(name):
            return {'message': 'Enter valid product name'}, 400

        sale = Salesrecord(name, price, category, quantitysold, amountbrought)

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

        sale = Salesrecord().get_id(id)

        if sale:
            return {"Salesrecord": sale.serialize()}

        return {'message': "Not found"}, 404
