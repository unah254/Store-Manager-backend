import json
import unittest
from flask import jsonify
from unittest import TestCase
from app import create_app


class TestProducts(TestCase):
    '''Test the products'''

    def setUp(self):
        """Define test variables and create an istance of a product"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.product_data = {
            "name": "Microphone",
            "price": 2500,
            "description": "suitable for podcast",
            "category": "Electronics"

        }
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

    def login_admin(self):
        """ method to login admin """
        data = {"email": "unah@admin.com",
                "password": "unah123",
                "admin":"True"
                }
        self.client.post(
            "api/v1/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"meassage": "succesfulyy logged"})

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

    def test_get_specific_product(self):
        ''' Test to get single product '''

        newproduct = self.client.post(
            "/api/v1/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json"}
        )
        response = self.client.get(
            "/api/v1/products/1", content_type='application/json')

        print(newproduct, response)

    def test_get_all_products(self):
        ''' Test to get all products '''

        response = self.client.get(
            "/api/v1/products", content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)


    def test_get_all_products_as_admin(self):
        """ Test all product items """

        token = self.get_token_as_admin()

        self.client.post(
            "/api/v1/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json"}
        )

        response = self.client.get(
            "api/v1/products",
            headers={"Authorization": f'Bearer {token}'}
        )

        self.assertEqual(response.status_code, 200)

    def test_add_new_products_as_admin(self):
        """ Test add product items """

        token = self.get_token_as_admin()

        self.client.post(
            "/api/v1/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )

        return jsonify({"message": "product added"}), 201

    def test_delete_products_as_admin(self):
        """ Test delete product items """

        token = self.get_token_as_admin()

        self.client.post(
            "/api/v1/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        self.client.delete(
            "/api/v1/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )

        return jsonify({"message": "product deleted"}), 201


class Testsales(TestCase):
    '''Test the sales'''

    def setUp(self):
        """Define test variables and create an istance of a record"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.record_data = {
            "name": "Microphone",
            "price": 2500,
            "quantity sold": 20,
            "category": "Electronics",
            "amount brought": 50000,
        }
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

    def login_admin(self):
        """ method to login admin """
        data = {"email": "unah@admin.com",
                "password": "unah123",
                "admin":"True"
                }
        self.client.post(
            "api/v1/login",
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )
        return jsonify({"meassage": "succesfulyy logged"})

    def get_token_as_admin(self):
        """get token """
        response = self.login_admin()
        token = json.loads(response.data).get("token", None)
        return token


    def get_token_as_user(self):
        """get token """
        self.signup()
        response = self.login()
        token = json.loads(response.data).get("token", None)
        return token

    def test_add_new_record_as_user(self):
        """ Test add product items """

        token = self.get_token_as_user()

        self.client.post(
            "/api/v1/products",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )

        return jsonify({"message": "product added"}), 201

    def test_get_all_records(self):
        ''' Test to get all records '''

        response = self.client.get(
            "/api/v1/sales", content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_get_specific_record(self):
        ''' Test to get single product '''

        newrecord = self.client.post(
            "/api/v1/sales",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json"}
        )
        response = self.client.get(
            "/api/v1/sales/1", content_type='application/json')

        print(newrecord, response)

    def test_invalid_product_description(self):
        ''' Test invalid product description '''

        product_data = {
            "name": "Valipro",
            "description": "****",
            "price": 20
        }

        self.client.post(
            "/api/v1/product",
            data=json.dumps(product_data),
            headers={"content-type": "application/json"}
        )
        return jsonify({"message": "enter valid product description"})

    def test_invalid_product_name(self):
        ''' Test invalid product description '''

        product_data = {
            "name": "****",
            "description": "suitable for podcast",
            "price": 20
        }

        self.client.post(
            "/api/v1/product",
            data=json.dumps(product_data),
            headers={"content-type": "application/json"}
        )
        return jsonify({"message": "enter valid product name"})

    def test_delete_records_as_admin(self):
        """ Test delete product items """

        token = self.get_token_as_admin()

        self.client.post(
            "/api/v1/sales",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        self.client.delete(
            "/api/v1/sales",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )

        return jsonify({"message": "record deleted"}), 201

    def test_delete_non_existing_record_as_admin(self):
        """ Test to delete non existing sale record  """
        token = self.get_token_as_admin()

        self.client.post(
            "/api/v1/sales",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json",
                     "Authorization": f'Bearer {token}'
                     }
        )
        self.client.delete(
            "api/v1/sales/1",
            headers={'content-type': 'application/json',
                     "Authorization": f'Bearer {token}'}
        )

        return jsonify({"message": "record does not exist"}), 404
def tearDown(self):
    self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
