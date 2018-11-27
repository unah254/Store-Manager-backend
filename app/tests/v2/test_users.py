import json
import unittest
from flask import jsonify
from unittest import TestCase
from app import create_app

from app.tests.v2.base_test import BaseTest
class TestUser(BaseTest):
    def test_email_exists(self):
        """ Test signup with an existing email """
        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        response = self.client.post(
            "api/v2/signup",
            data=json.dumps(self.email_exists_data),
            headers={'content-type': 'application/json',
                    "Authorization": 'Bearer {}'.format(token)
                    }
        )
        self.assertEqual(response.status_code, 400)

    def test_non_existing_user_login(self):
        """ Test if user does not exist """

        self.signup()

        response = self.client.post(
            "api/v2/login",
            data=json.dumps(self.non_existing_user_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 404)
        print(json.loads(response.data.decode('utf-8'))['message'], ">>>>>>>>")

        self.assertEqual(json.loads(response.data.decode('utf-8'))["message"], "user not found")

    def test_register_user(self):
        """ Test invalid email """
        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        response = self.client.post(
            "api/v2/signup",
            data=json.dumps(self.register_email_data),
            headers={'content-type': 'application/json',
            "Authorization": 'Bearer {}'.format(token)
            }
        )
        res = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)
        self.assertEqual(res['message'], 'user attendant@gmail.com created successfully' )
        self.assertEqual(response.content_type, 'application/json')

    def test_invalid_password(self):


        response = self.client.post(
            "api/v2/login",
            data=json.dumps(self.invalid_password_data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 404)


    def test_incorect_password(self):

        self.signup()
        response = self.client.post(
            "api/v2/login",
            data=json.dumps(self.incorects_pass_data),
            headers={'content-type': 'application/json'}
        )

        self.assertEqual(response.status_code, 404)

    def test_non_existing_email(self):
        """ Test non existing email """
        data = {
            "email": "gmoh@user.com",
            "password": "Unah127"
        }

        response = self.client.post(
            "api/v2/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(res['message'], "user not found")
        self.assertEqual(response.content_type, 'application/json')

    def test_logout_user(self):
        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        response = self.client.post(
            "api/v2/logout",
            # data=json.dumps(self.register_email_data),
            headers={'content-type': 'application/json',
            "Authorization": 'Bearer {}'.format(token)
            }
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], 'successfuly logged out')

    def test_valid_email(self):
        response = self.client.post(
            "api/v2/login",
            data=json.dumps(self.invalid_email_data),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(response.status_code, 400)

    def test_promote_non_existing_user(self):  
        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')
  
        response = self.client.put(
            "/api/v2/user/1",
            data=json.dumps(self.non_existing_user_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        ''' Test to get all users '''
        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        self.client.post(
            "/api/v2/signup",
            data=json.dumps(self.signup_data),
            content_type="application/json",
            headers={
                "Authorization": 'Bearer '+token
            }
        )
        response = self.client.get(
            "/api/v2/users",
            content_type='application/json',
            headers={
                "Authorization": 'Bearer '+token
            }
        )

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 404)
        
if __name__ == "__main__":
    unittest.main()