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

        # connect to storemanagertest database
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

        # update table products set category = 'food' where product_id = 10;
class User(StoreDatabase):

    def __init__(self, email=None, password=None, admin=False):
            super().__init__()
            self.email = email
            if password:
                self.password_hash = generate_password_hash(password)
                self.admin = admin

    def create(self, schema):
        """ create table users """
        self.create_table(
            """
            CREATE TABLE users(
                id serial PRIMARY KEY,
                email  VARCHAR NOT NULL,
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
        SQL = "INSERT INTO users(email, password, admin) VALUES( %s, %s, %s, %s)"
        data = (self.email, self.password_hash, self.admin)
        self.cur.execute(SQL, data)
        self.save()

    def map_user(self, data):
        """ map user to an object"""

        self.id = data[0]
        self.email = data[2]
        self.password_hash = data[3]
        self.admin = data[4]

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
