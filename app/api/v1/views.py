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
        category = ['category']

        if not Validators().valid_product_name(name):
            return {'message': 'Enter valid product name'}, 400
        if not Validators().valid_product_description(description):
            return {'message': 'Enter valid product description'}, 400

        product = Product(name, price, description, category)

        products.append(product)

        return {"message": "product added"}, 201
