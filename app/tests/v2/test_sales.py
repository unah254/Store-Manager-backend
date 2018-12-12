import json
import unittest
import json
from flask import jsonify
from unittest import TestCase
from app import create_app
from app.api.v2.models import StoreDatabase
from app.tests.v2.base_test import BaseTest
from database import migrate, drop, create_admin


class Testsales(BaseTest):
    '''Test the sales'''

    def test_add_new_record_as_attendant(self):
        """ Test add product items """

        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        response = self.client.post(
            "/api/v2/signup",
            data=json.dumps(self.signup_data),
            content_type="application/json",
            headers={
                "Authorization": 'Bearer '+token
            }
        )
        signin = self.login_user()
        token = json.loads(signin.data.decode()).get('token')

        responses = self.client.post(
            "api/v2/sales",
            data=json.dumps(self.record_data),
            content_type="application/json",
            headers={
                "Authorization": 'Bearer '+token
            }
        )
        res = json.loads(responses.data.decode())

        self.assertEqual(response.status_code, 201)

    def test_get_all_records(self):
        ''' Test to get all records '''
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
            "/api/v2/sales",
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
