import os
import unittest
import json
import psycopg2
from app import create_app

from database import migrate, drop, create_admin


class BaseTest(unittest.TestCase):
    drop()

    def setUp(self):
        """ setting up tests """

        self.app = create_app(os.getenv('APP_SETTINGS'))
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app.app_context():
            drop()
            migrate()
            create_admin()

        self.login_attendant_data = {
            "email": "userme@gmail.com",
            "password": "Unah1234",
            "admin": False
        }
        self.login_admin_data = {
            "email": "unahgrace@gmail.com",
            "password": "Unah123"
        }
        self.signup_data = {
            "email": "userme@gmail.com",
            "password": "Unah1234",
            "admin": False
        }
        self.email_exists_data = {
            "email": "unahgrace@gmail.com",
            "password": "Unah123",
            "admin": True
        }

        self.invalid_product_name = {
            "name": "***********1",
            "category": "electronics",
            "price": 2500,
            "quantity": 15
        }

        self.incorects_pass_data = {
            "email": "unah@gmail.com",
            "password": "Kimame1235"
        }

        self.invalid_password_data = {
            "email": "mwanzia@gmail.com",
            "password": "nht"
        }

        self.register_email_data = {
            "email": "attendant@gmail.com",
            "password": "User123",
            "admin": "False"
        }
        self.user_doest_not_exist_data = {
            "email": "user20",
            "password": "Ramo123"
        }
        self.product_data = {
            "name": "hjjkjrrhjjkkjky",
            "category": "electronicsgfdf",
            "price": 2500
        }
        self.record_data = {
            "product_id": 1,
            "creator_name": "meme",
            "quantity_to_sell": 10,
        }
        self.product_admin_data = {
            "name": "thsisisme",
            "category": "clothing",
            "price": 2500,
            "quantity": 10,
        }
        self.product_test_data = {
            "name": "mememe",
            "category": "electronicsgfdf",
            "price": 2500,
            "quantity": 20
        }
        self.non_existing_user_data = {
            "email": "hello@gmail.com",
            "password": "Me1243",
            "admin": "false"
        }
        self.invalid_email_data = {
            "email": "unahgracegmail.com",
            "password": "Unah123"
        }

    def signup(self):
        """ signup method"""

        response = self.client.post(
            "api/v2/signup",
            data=json.dumps(self.signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login_admin(self):
        """ method to login admin """

        res = self.client.post(
            "api/v2/login",
            data=json.dumps(self.login_admin_data),
            headers={'content-type': 'application/json'}
        )

        return res

    def login_user(self):
        """ login method """

        response = self.client.post(
            "api/v2/login",
            data=json.dumps(self.login_attendant_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token_as_admin(self):
        """get token """
        token = self.login_admin()
        return token
