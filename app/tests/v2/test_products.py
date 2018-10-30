import json
import unittest
import json
from flask import jsonify
from unittest import TestCase
from app import create_app
from app.api.v2.models import StoreDatabase
from app.tests.v2.base_test import BaseTest
from database import migrate, drop, create_admin

class TestProducts(BaseTest):
    '''Test the products'''
    def test_add_new_products_as_admin(self):
        """ Test add product items """

        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        response = self.client.post(
            "/api/v2/product",
            data=json.dumps(self.product_admin_data),
            content_type="application/json",
            headers={
                     "Authorization": 'Bearer '+token
                     }
        )
        res = json.loads(response.data.decode())
        
        self.assertEqual(response.status_code, 201)
       
    def test_get_specific_product(self):
        ''' Test to get single product '''

        newproduct = self.client.post(
            "/api/v2/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json"}
        )
        response = self.client.get(
            "/api/v2/products/1", content_type='application/json')

        print(newproduct, response)

    def test_get_all_products(self):
        ''' Test to get all products '''

        response = self.client.get(
            "/api/v2/products", content_type='application/json')

        # data = json.loads(response.data.decode('utf-8'))
       
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)


    def test_get_all_products_as_admin(self):
        """ Test all product items """

        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        self.client.post(
            "/api/v2/product",
            data=json.dumps(self.product_test_data),
            content_type="application/json",
            headers={
                     "Authorization": 'Bearer '+token
                     }
        )

        response = self.client.get(
            "api/v2/products",
            content_type="application/json",
            headers={
                     "Authorization": 'Bearer '+token
                     }
        )
        res = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(res['message'], "success")
        self.assertEqual(response.content_type, 'application/json')

    def test_delete_products_as_admin(self):
        """ Test delete product items """
        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        self.client.post(
            "/api/v2/product",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        response = self.client.delete(
            "/api/v2/products/1",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
    def test_invalid_product_name(self):
        ''' Test invalid product description '''

        login = self.login_admin()
        token = json.loads(login.data.decode()).get('token')

        response = self.client.post(
            "/api/v2/product",
            data=json.dumps(self.invalid_product_name),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        self.assertEqual(response.status_code, 400)
        print(response)

# class Testsales(BaseTest):
#     '''Test the sales'''

    # def test_get_all_records(self):
    #     ''' Test to get all records '''

    #     response = self.client.get(
    #         "/api/v2/sales", content_type='application/json')

    #     data = json.loads(response.data.decode('utf-8'))
    #     print(data)
    #     self.assertEqual(response.content_type, 'application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotEqual(response.status_code, 404)

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
