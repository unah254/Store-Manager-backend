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
        token = json.loads(signin.data.decode()).get ('token')
        
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
        # self.assertEqual(res['message'], "product does not exist")

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
        self.assertEqual(response.status_code, 401)
        self.assertNotEqual(response.status_code, 404)

    # def test_get_specific_record(self):
    #     ''' Test to get single product '''

    #     newrecord = self.client.post(
    #         "/api/v2/sales",
    #         data=json.dumps(self.record_data),
    #         headers={"content-type": "application/json"}
    #     )
    #     response = self.client.get(
    #         "/api/v2/sales/1", content_type='application/json')

    #     print(newrecord, response)


    
    # def test_delete_records_as_admin(self):
    #     """ Test delete product items """

    #     data = self.login_admin()
    #     token = data['token']

    #     self.client.post(
    #         "/api/v2/sales",
    #         data=json.dumps(self.record_data),
    #         headers={"content-type": "application/json",
    #                  "Authorization": f'Bearer {token}'
    #                  }
    #     )
    #     response = self.client.delete(
    #         "/api/v2/sales/1",
    #         data=json.dumps(self.record_data),
    #         headers={"content-type": "application/json",
    #                  "Authorization": f'Bearer {token}'
    #                  }
    #     )

    #     self.assertEqual(response.status_code, 404)

    # def test_delete_non_existing_record_as_admin(self):
    #     """ Test to delete non existing sale record  """
    #     data = self.login_admin()
    #     token = data['token']

    #     self.client.post(
    #         "/api/v2/sales",
    #         data=json.dumps(self.record_data),
    #         headers={"content-type": "application/json",
    #                  "Authorization": f'Bearer {token}'
    #                  }
    #     )
    #     response = self.client.delete(
    #         "api/v1/sales/1",
    #         headers={'content-type': 'application/json',
    #                  "Authorization": f'Bearer {token}'}
    #     )

    #     self.assertEqual(response.status_code, 404)



if __name__ == "__main__":
    unittest.main()
