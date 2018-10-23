import json
import unittest
from flask import jsonify
from unittest import TestCase
from app import create_app


class TestUser(unittest.TestCase):

    def setUp(self):
        """ setting up testing """

        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """ Teardown """
        self.app_context.pop()

    def signup(self):
        """ signup method"""
        signup_data = {
            "email": "greisunah@admin.com",
            "password": "Unah1234",
            "is_admin": 1
        }
        response = self.client.post(
            "api/v1/signup",
            data=json.dumps(signup_data),
            headers={'content-type': 'application/json'}
        )
        return response

    def login(self):
        """ login method """
        login_data = {
            "email": "greisunah@admin.com",
            "password": "Unah1234"
        }
        response = self.client.post(
            "api/v1/login",
            data=json.dumps(login_data),
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
        response = self.login_admin()
        token = json.loads(response.data).get("token", None)
        return token

    def test_email_exists(self):
        """ Test signup with an existing email """
        email_exists_data = {
            "email": "sifuma@gmail.com",
            "password": "Sify1235",
            "admin": 1
        }
        self.login_admin()

        self.client.post(
            "api/v1/signup",
            data=json.dumps(email_exists_data),
            headers={'content-type': 'application/json'}
        )

    
    def login_admin(self):
        """ method to login admin """
        data = {"email": "unah@admin.com",
                "password": "unah123",
                "admin":"True"
                }
        res = self.client.post(
            "http://127.0.0.1:5000/api/v1/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        print (res, "ghjkdk")

        return res

    

    def test_non_existing_user_login(self):
        """ Test if user does not exist """
        non_existing_user_data = {
            "email": "greisunah@user.com",
            "password": "Unah127"
        }

        self.signup()

        response = self.client.post(
            "api/v1/login",
            data=json.dumps(non_existing_user_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user not found")

    def test_invalid_email(self):
        """ Test invalid email """
        invalid_email_data = {
            "email": "greisunah",
            "password": "Unah127"
        }

        self.client.post(
            "api/v2/signup",
            data=json.dumps(invalid_email_data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"meassage": "enter a valid email"})

        
    def test_invalid_password(self):
        invalid_password_data = {
            "email": "kraftymal@gmail.com",
            "password": "krafty123",
            "is_admin": 1
        }

        self.client.post(
            "api/v1/signup",
            data=json.dumps(invalid_password_data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"message": "password should start with a capital"
                        " letter and include a number"})

    def test_incorect_password(self):
        """ test for incorect password """
        self.incorects_pass_data = {
            "username": "kimame",
            "password": "Kimame1235"
        }
        self.signup()
        self.client.post(
            "api/v1/login",
            data=json.dumps(self.incorects_pass_data),
            headers={'content-type': 'application/json'}
        )

        return jsonify({"message": "password is incorrect"})

    def test_non_existing_email(self):
        """ Test non existing email """
        data = {
            "email": "gmoh@user.com",
            "password": "Unah127"
        }

        self.client.post(
            "api/v1/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"meassage": "email does not exist"})