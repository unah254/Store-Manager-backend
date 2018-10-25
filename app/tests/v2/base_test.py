import unittest
import json

from app import create_app

from database import migrate, drop, create_admin

class BaseTest(unittest.TestCase):
    def setUp(self):
        """ setting up tests """

        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        with self.app.app_context():
            drop()
            migrate()
            create_admin()
        
        self.login_data = {
            "email": "greisunah@admin.com",
            "password": "Unah1234"
        }
        self.login_admin_data = {
            "email":"admin@gmail.com",
	        "password":"sifuma123"
        }
        
        self.invalid_product_name = {
            "name": "***********1",
            "category": "electronics",
            "price": 2500
        }

        self.incorects_pass_data = {
            "email": "unah@gmail.com",
            "password": "Kimame1235"
        }

        self.invalid_password_data = {
            "email": "mwanzia@gmail.com",
            "password": "mandie123"
        }

        self.invalid_email_data = {
            "email": "me",
            "password": "Sifuma123",
            "admin": "True"
        }
        self.user_doest_not_exist_data = {
            "email": "user20",
            "password": "Ramo123"
        }

    def login_admin(self):
        """ method to login admin """
        
        res = self.client.post(
            "api/v2/login",
            data=json.dumps(self.login_admin_data),
            headers={'content-type': 'application/json'}
        )
        data = json.loads(res.data.decode())
        return data
    def login_user(self):
        """ login method """
        
        response = self.client.post(
            "api/v2/login",
            data=json.loads(self.login_data),
            headers={'content-type': 'application/json'}
        )
        return response
    # def logout(self):
    #     """ logout method """
        
    


    def get_token_as_admin(self):
        """get token """
        token = self.login_admin()
        return token