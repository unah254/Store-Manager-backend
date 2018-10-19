from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from flask_jwt_extended import create_access_token

from jwt import ExpiredSignatureError, InvalidTokenError

# imported module to validate the inputs
from .utils import Validators

# list to store products
products = []



class Product:
    '''product class to initialize products and display in json'''
    def __init__(self, name=None, price=None, category=None):
        '''create an instance of a new product'''
        self.id = len(products)+1
        self.name = name
        self.price = price
        self.category = category

    def serialize(self):
        '''to get created data and display in json format'''
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category
        )

    def get_id(self, product_id):
        '''display specific product id'''
        for product in products:
            if product.id == product_id:
                return product

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
Users = []
class User:

    user_id = 1

    def __init__(self, email=None, password=None,
                 is_admin=None):

        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.id = User.user_id

        User.user_id += 1


    def get_by_email(self, email):
        for user in Users:
            if user.email == email:
                return user