from flask import Flask
from werkzeug.security import generate_password_hash




# imported module to validate the inputs
from .utils import Validators

# list to store products
PRODUCTS = []



class Product:
    '''product class to initialize products and display in json'''
    def __init__(self, name=None, price=None, category=None):
        '''create an instance of a new product'''
        self.id = len(PRODUCTS)+1
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
        for product in PRODUCTS:
            if product.id == product_id:
                return product

sales=[]

class Salesrecord:
    '''sales class to initialize records and display in json'''
    
    sale_record_id = 1
    
    def __init__(self, name=None, price=None, category=None, quantitysold=None, amountbrought=None):
        '''create an instance of a new sale record'''
        self.id = Salesrecord.sale_record_id
        self.name = name
        self.price = price
        self.category = category
        self.quantitysold = quantitysold
        self.amountbrought = amountbrought

        Salesrecord.sale_record_id += 1

    def serialize(self):
        ''' serialize a Salesrecord object to a dictionary'''
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category,
            quantitysold=self.quantitysold,
            amountbrought=self.amountbrought
        )

    def get_by_id(self, sales_id):
        '''get records by id'''
        for Salesrecord in sales:
            if Salesrecord.id == sales_id:
                return Salesrecord
Users = []

class User:

    user_id = 1

    def __init__(self, email="grace@admin.com", password="123ht",
                 is_admin=True):

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