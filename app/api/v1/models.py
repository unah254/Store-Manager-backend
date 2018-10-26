from flask import Flask
from werkzeug.security import generate_password_hash




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
    def create_product(self):

        new_product = { 'id':self.id, 'name':self.name,'price':self.price,'category':self.category}
        products.append(new_product)
        return products
    @staticmethod
    def get_all_product():

        return products

    def serialize(self):
        '''to get created data and display in json format'''
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category
        )

    def get_id(self, id):
        '''display specific product id'''

        product_index= id - 1

        return products[product_index]
sales=[]

class Salesrecord:
    '''sales class to initialize records and display in json'''
    
    sale_record_id = 1
    
    def __init__(self, name=None, price=None, quantitysold=None, amountbrought=None):
        '''create an instance of a new sale record'''
        self.id = Salesrecord.sale_record_id
        self.name = name
        self.price = price
        self.quantitysold = quantitysold
        self.amountbrought = amountbrought

        Salesrecord.sale_record_id += 1
    def create_record(self):

        new_record = { 'id':self.id, 'name':self.name,'price':self.price,'quantitysold':self.quantitysold, 'amountbrought':self.amountbrought}
        sales.append(new_record)
        return sales

    @staticmethod
    def get_all_record():

        return sales

    def serialize(self):
        ''' serialize a Salesrecord object to a dictionary'''
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            quantitysold=self.quantitysold,
            amountbrought=self.amountbrought
        )

    def get_by_id(self, sales_id):
        '''get records by id'''
        record_index= id - 1

        return sales[record_index]
Users = []

class User:

    user_id = 1

    def __init__(self, email=None, password=None,
                 admin=False):

        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.admin = admin
        self.id = User.user_id

        User.user_id += 1


    def get_by_email(self, email):
        for user in Users:
            if user.email == email:
                return user
