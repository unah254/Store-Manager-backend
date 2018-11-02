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
        self.assertEqual(res['message'], "product successfuly created")

       
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
        self.assertEqual(response.status_code, 404)
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
     
    

   

    

if __name__ == "__main__":
    unittest.main()
