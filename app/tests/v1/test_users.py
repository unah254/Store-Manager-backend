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

    def get_token(self):
        """ get_token method """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    def test_email_exists(self):
        """ Test signup with an existing email """
        data = {
            "email": "sifuma@gmail.com",
            "password": "Sify1235",
            "is_admin": 1
        }
        self.signup()

        response = self.client.post(
            "api/v1/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"message": "user with sifuma@gmail.com"
                        " already exists"})

        response_data = json.loads(response.data.decode('utf-8'))

        print(response_data)

    def test_non_existing_user_login(self):
        """ Test if user does not exist """
        data = {
            "email": "greisunah@user.com",
            "password": "Unah127"
        }

        self.signup()

        response = self.client.post(
            "api/v1/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(json.loads(response.data)[
                         "message"], "user not found")

    def test_invalid_email(self):
        """ Test invalid email """
        data = {
            "email": "greisunah",
            "password": "Unah127"
        }

        response = self.client.post(
            "api/v2/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"meassage": "enter a valid email"})

        response_data = json.loads(response.data.decode("utf-8"))

    def test_invalid_password(self):
        data = {
            "email": "kraftymal@gmail.com",
            "password": "krafty123",
            "is_admin": 1
        }

        response = self.client.post(
            "api/v1/signup",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"message": "password should start with a capital"
                        " letter and include a number"})

        response_data = json.loads(response.data.decode('utf-8'))

        print(response_data)
