import unittest
import json

from app import create_app

from app.api.v1.models import User

class BaseTest(unittest.TestCase):
    def setUp(self):
        """ setting up tests """

        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.product_data = {
            "name": "microphone",
            "price": 2500,
            "category": "electronics"

        }
        self.signup_data = {
            "email": "greisunah@admin.com",
            "password": "Unah1234",
            "admin": "False"
        }
        self.login_admin_data = {
            "email":"admin@gmail.com",
	        "password":"sifuma123"
        }
        self.login_data = {
            "email": "greisunah@admin.com",
            "password": "Unah1234"
        }
        self.email_exists_data = {
            "email": "sifuma@gmail.com",
            "password": "Sify1235",
            "admin": 1
        }
        self.record_data = {
            "name": "Microphone",
            "price": 2500,
            "quantity sold": 20,
            "amount brought": 50000,
        }
        self.invalid_product_data = {
            "name": "****",
            "category": "electronics",
            "price": 20
        }
        self.invalid_product_description = {
            "id":1,
            "name": "Valipro",
            "description": "****",
            "price": 20
        }
        self.invalid_email_data = {
            "email": "greisunah",
            "password": "Unah127"
        }
        self.invalid_password_data = {
            "email": "kraftymal@gmail.com",
            "password": "krafty123",
        }
        self.non_existing_user_data = {
            "email": "greisunah@user.com",
            "password": "Unah127"
        }
        self.incorects_pass_data = {
            "username": "kimame",
            "password": "Kimame1235"
        }
    def signup(self):
        """ signup method"""
       
        response = self.client.post(
            "api/v1/signup",
            data=json.dumps(self.signup_data),
            headers={'content-type': 'application/json'}
        )
        return response
    def login_admin(self):
        """ method to login admin """
        
        res = self.client.post(
            "api/v1/login",
            data=json.dumps(self.login_admin_data),
            headers={'content-type': 'application/json'}
        )
        data = json.loads(res.data.decode())
        return data

    def login(self):
        """ login method """
        
        response = self.client.post(
            "api/v1/login",
            data=json.loads(self.login_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def get_token_as_user(self):
        """get token """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    def get_token_as_admin(self):
        """get token """
        token = self.login_admin()
        return token
    # def authenticate_admin(self):
    #     response = self.client.post("api/v1/login", data = json.dumps(self.login_admin_data))

    #     access_token = json.loads(response.data).get("token", None)

    #     return access_token
        