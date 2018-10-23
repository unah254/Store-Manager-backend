import json
import unittest
from flask import jsonify
from unittest import TestCase
from app import create_app

from app.tests.v1.base_test import BaseTest
class TestUser(BaseTest):


    def test_email_exists(self):
        """ Test signup with an existing email """
        data = self.login_admin()

        token = data['token']

        response = self.client.post(
            "api/v1/signup",
            data=json.dumps(self.email_exists_data),
            headers={'content-type': 'application/json',
                    "Authorization": f'Bearer {token}'
                    }
        )
        self.assertEqual(response.status_code, 201)
        
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
        data = self.login_admin()

        token = data['token']

        response = self.client.post(
            "api/v1/signup",
            data=json.dumps(self.invalid_email_data),
            headers={'content-type': 'application/json',
            "Authorization": f'Bearer {token}'
            }
        )
        self.assertEqual(response.status_code, 400)

        
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
        
        self.signup()
        response = self.client.post(
            "api/v1/login",
            data=json.dumps(self.incorects_pass_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 400)

    def test_non_existing_email(self):
        """ Test non existing email """
        data = {
            "email": "gmoh@user.com",
            "password": "Unah127"
        }

        response = self.client.post(
            "api/v1/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 404)