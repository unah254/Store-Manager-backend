import os
import psycopg2

from datetime import datetime
from werkzeug.security import generate_password_hash

config_name = os.environ['APP_SETTINGS']


class StoreDatabase:
    """ database connection model """

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")

        self.conn = psycopg2.connect(self.db_url)

        self.cur = self.conn.cursor()

    def create_table(self, schema):
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

    def random(self, data):
        """ serialize a user to a dictionary """
        return dict(
            email=data[1],
            password=data[2],
            admin=data[3]

        )

    def fetch_by_id(self, _id):
        """ fetch user by id """
        self.cur.execute(
            "SELECT * FROM users where id = %s", (_id, ))
        user = self.cur.fetchone()

        self.save()

        if user:
            return self.random(user)
        return None

    def update(self, id, email, password, admin):
        """ promote a user """

        self.cur.execute(
            """ UPDATE users SET email =%s, password=%s, admin =%s WHERE id = %s """, (
                email, password, admin, id,)
        )
        self.save()

        return self.fetch_by_id(id)

    def delete_user(self, user_id):
        """  deleting a user"""
        self.cur.execute(
            "DELETE FROM users WHERE id = %s", (user_id, )
        )
        self.save()
        self.close()
    def fetch_all_users(self):
        """ fetch all  users """
        self.cur.execute("SELECT * FROM users")
        users = self.cur.fetchall()
        self.save()
        self.close()

        if users:
            return [self.map_user(user) for user in users]
        return None

class ProductItem(StoreDatabase):

    def __init__(self, name=None, category=None, price=None, quantity=None):
        super().__init__()
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.date = datetime.now().replace(second=0, microsecond=0)

    def create(self):
        """ create table productitems """
        self.create_table(
            """
            CREATE TABLE IF NOT EXISTS productitems (
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                category TEXT,
                price INTEGER,
                quantity INTEGER,
                date  TIMESTAMP
            );
            """
        )

    def drop(self):
        """ drop if table exists """
        self.drop_table('productitems')

    def add(self):
        """ add productitem to table"""

        SQL = "INSERT INTO productitems(name, category, price, quantity, date) VALUES (%s, %s, %s,%s, %s)"
        data = (self.name, self.category, self.price, self.quantity, self.date)
        self.cur.execute(SQL, data)
        self.save()

    def map_productitems(self, data):
        """ map productitem to an object"""
        productitem = ProductItem(
            name=data[1], category=data[2], price=data[3], quantity=data[4])
        productitem.id = data[0]
        productitem.date = data[4]
        self = productitem

        return self

    def serialize(self):
        """ serialize a ProductItem object to a dictionary"""
        return dict(
            name=self.name,
            category=self.category,
            date=str(self.date),
            price=self.price,
            quantity=self.quantity
        )

    def random(self, data):
        """ serialize a ProductItem object to a dictionary"""
        return dict(
            name=data[1],
            category=data[2],
            date=str(self.date),
            price=data[3],
            quantity=data[4]
        )

    def fetch_by_id(self, _id):
        """ fetch product by id """
        self.cur.execute(
            "SELECT * FROM productitems where id = %s", (_id, ))
        product_item = self.cur.fetchone()

        self.save()

        if product_item:

            return self.random(product_item)
        return None

    def fetch_by_name(self, name):
        """ fetch product by name """
        self.cur.execute(
            "SELECT * FROM productitems where name = %s", (name, ))
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

    def update(self, id, name, price, category, quantity):
        """ update an existing product item """
        self.cur.execute(
            """ UPDATE productitems SET name =%s, category =%s, price=%s, quantity =%s WHERE id = %s """, (
                name, category, price, quantity, id,)
        )
        self.save()

        return self.fetch_by_id(id)

    def fetch_all_productitems(self):
        """ fetch all product items """
        self.cur.execute("SELECT * FROM productitems")
        productitems = self.cur.fetchall()
        self.save()
        self.close()

        if productitems:
            return [self.map_productitems(productitem) 
            for productitem in productitems]
        return None


class SalesRecord(StoreDatabase):

    def __init__(self, product_id=None, price=None, creator_name=None, quantity_to_sell=None,):
        super().__init__()
        self.product_id = product_id
        self.price = price
        self.quantity_to_sell = quantity_to_sell
        self.creator_name = creator_name
        self.date = datetime.now().replace(second=0, microsecond=0)

    def create(self):
        """ create table salerecords """
        self.create_table(
            """
            CREATE TABLE sales (
                id serial PRIMARY KEY,
                price INTEGER,
                creator_name VARCHAR NOT NULL,
                product_id INTEGER,
                quantity_to_sell INTEGER,   
                date  TIMESTAMP
            );
            """
        )

    def drop(self):
        """ drop if table exists """
        self.drop_table('sales')

    def create_sales(self, product_id, price, quantity_to_sell, creator_name):
        """ add salerecord to table"""
        self.cur.execute(
            "SELECT * FROM productitems WHERE id = %s;", (product_id,))
        quantity_available = self.cur.fetchone()

        self.save()

        if quantity_available:

            SQL = "INSERT INTO sales(product_id, price,  creator_name, quantity_to_sell, date) VALUES (%s, %s, %s, %s, %s)"

            data = (self.product_id, self.price, self.creator_name,
                    self.quantity_to_sell, self.date)

            self.cur.execute(SQL, data)
            self.save()

            remaining_quantity = int(
                quantity_available[4]) - int(quantity_to_sell)

            self.cur.execute(
                "UPDATE productitems SET quantity=%s WHERE id=%s", (
                    remaining_quantity, product_id)
            )
            self.save()

    def map_salesrecord(self, data):
        """ map salerecord to an object"""
        salerecord = SalesRecord(
            creator_name=data[1], product_id=data[2], price=data[3], quantity_to_sell=data[4])
        SalesRecord.id = data[0]
        SalesRecord.date = data[5]
        self = salerecord

        return self

    def serialize(self):
        """ serialize a SalesRecord object to a dictionary"""
        return dict(
            creator_name=self.creator_name,
            product_id=self.product_id,
            price=self.price,
            quantity_to_sell=self.quantity_to_sell,
            date=str(self.date),

        )

    def fetch_record_by_id(self, _id):
        """ fetch record by id """
        self.cur.execute(
            "SELECT * FROM sales where id = %s", (_id, ))
        record = self.cur.fetchone()
        self.save()
        self.close()

        if record:
            return self.map_salesrecord(record)
        return None

    def fetch_by_name(self, name):
        """ fetch record by name """
        self.cur.execute("SELECT * FROM sales where name = %s", (name,))
        record = self.cur.fetchone()

        if record:
            return self.map_salesrecord(record)
        return None

    def delete(self, record_id):
        """ delete sales record """

        self.cur.execute(
            "DELETE FROM sales WHERE id = %s", (record_id, )
        )
        self.save()
        self.close()

    def fetch_by_id(self, _id):
        """ fetch product by id """
        self.cur.execute(
            "SELECT * FROM productitems where id = %s", (_id, ))
        product_item = self.cur.fetchone()
        self.save()
        self.close()

        if product_item:
            return self.map_salesrecord(product_item)
        return None

    def fetch_all_salesrecords(self):
        """ fetch all  sales record """
        self.cur.execute("SELECT * FROM sales")
        salerecord = self.cur.fetchall()
        self.save()
        self.close()

        if salerecord:
            return [self.map_salesrecord(productitem) for productitem in salerecord]
        return None
