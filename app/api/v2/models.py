from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2

from flask import current_app


class StoreDatabase:
    """ database connection model """

    def __init__(self):
        self.db_host = current_app.config['DB_HOST']
        self.db_username = current_app.config['DB_USERNAME']
        self.db_password = current_app.config['DB_PASSWORD']
        self.db_name = current_app.config['DB_NAME']

        # connect to storemanagerapp database
        self.conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_username,
            password=self.db_password,
            database=self.db_name,
        )
        # open cursor to enable operation of database
        self.cur = self.conn.cursor()

    def create_table(self,schema):
        """ method to create a table """
        self.cur.execute(schema)
        self.save()

    def drop_table(self, name):
        """ method to drop a table """
        self.cur.execute("DROP TABLE IF EXISTS " + name)
        self.save()

    def save(self):
        """ method to save any changes made """
        self.conn.commit()

    def close(self):
        self.cur.close()

Users=[]       
class User(StoreDatabase):

    def __init__(self, email=None, password=None, admin=False):
            super().__init__()
            self.email = email
            if password:
                self.password_hash = generate_password_hash(password)
                self.admin = admin

    def create(self):
        """ create table users_table """
        self.create_table(
            """
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                email  VARCHAR NOT NULL UNIQUE, 
                password VARCHAR NOT NULL,
                admin BOOLEAN NOT NULL
            );
            """
        )

    def drop(self):
        """ drop table if exists """
        self.drop_table('users')

    def add(self):
        """ add users to table"""
        SQL = "INSERT INTO users(email, password, admin) VALUES( %s, %s, %s)"
        data = (self.email, self.password_hash, self.admin)
        self.cur.execute(SQL, data)
        self.save()

    def map_user(self, data):
        """ map user to an object"""

        self.id = data[0]
        self.email = data[1]
        self.password_hash = data[2]
        self.admin = data[3]

        return self

    def fetch_by_email(self, email):
        """ fetch user by email """
        self.cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = self.cur.fetchone()

        if user:
            return self.map_user(user)
        return None

    def serialize(self):
        """ serialize a user to a dictionary """
        return dict(
            id=self.id,
            email=self.email,
            password_hash=self.password_hash,
            admin=self.admin
        )
    def delete_user(self, user_id):
        """  deleting a user"""
        self.cur.execute(
            "DELETE FROM users WHERE id = %s", (user_id, )
        )
        self.save()
        self.close()

Products=[]
class ProductItem(StoreDatabase):
    
    def __init__(self, name=None, category=None, price=None):
        super().__init__()
        self.id=0
        self.name = name
        self.category = category
        self.price = price
        self.date = datetime.now().replace(second=0, microsecond=0)

    def create(self):
        """ create table productitems """
        self.create_table(
            """
            CREATE TABLE productitems (
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                category TEXT,
                price INTEGER,
                date  TIMESTAMP
            );
            """
        )

    def drop(self):
        """ drop if table exists """
        self.drop_table('productitems')

    def add(self):
        """ add productitem to table"""
        
        SQL = "INSERT INTO productitems(name, category, price, date) VALUES (%s, %s, %s,%s )"
        data = (self.name, self.category, self.price, self.date)
        self.cur.execute(SQL, data)
        self.save()

    def map_productitems(self, data):
        """ map productitem to an object"""
        productitem = ProductItem(
            name=data[1], category=data[2], price=data[3])
        productitem.id = data[0]
        productitem.date = data[4]
        self = productitem

        return self

    def serialize(self):
        """ serialize a ProductItem object to a dictionary"""
        return dict(
            id=self.id,
            name=self.name,
            category=self.category,
            date=str(self.date),
            price=self.price,
        )

    def fetch_by_id(self, _id):
        """ fetch product by id """
        self.cur.execute(
            "SELECT * FROM productitems where id = %s", (_id, ))
        product_item = self.cur.fetchone()
        self.save()
        self.close()

        if product_item:
            return self.map_productitems(product_item)
        return None

    def fetch_by_name(self, name):
        """ fetch product by name """
        self.cur.execute("SELECT * FROM productitems where name = %s", (name,))
        product_item = self.cur.fetchone()

        if product_item:
            return self.map_productitems(product_item)
        return None

    def delete(self, product_id):
        """ delete product item """

        self.cur.execute(
            "DELETE FROM productitems WHERE id = %s", (product_id, )
        )
        self.save()
        self.close()

    def update(self, product_id,name, price, category):
        """ update an existing product item """

        self.cur.execute(
            """ UPDATE productitems SET name =%s, category =%s, price=%s WHERE id = %s """, (
                name, category, price, product_id,)
        )
        self.save()
        self.close()

    def fetch_all_productitems(self):
        """ fetch all product items """
        self.cur.execute("SELECT * FROM productitems")
        productitems = self.cur.fetchall()
        self.save()
        self.close()

        if productitems:
            return [self.map_productitems(productitem) for productitem in productitems]
        return None
