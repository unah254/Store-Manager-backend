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

    def test_add_new_product(self):
        ''' Test to add new product '''

        self.client.post(
            "/api/v1/products",
            data=json.dumps(self.product_data),
            headers={"content-type": "application/json"}
        )
        return jsonify({"message": "product added"}), 201


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

    def test_create_new_sale_record(self):
        ''' Test to write new sale record '''

        self.client.post(
            "/api/v1/sales",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json"}
        )
        return jsonify({"message": "record created"}), 201

    def test_get_all_records(self):
        ''' Test to get all records '''

        response = self.client.get(
            "/api/v1/sales", content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_invalid_product_description(self):
        ''' Test invalid product description '''

        product_data = {
            "name":"Valipro",
            "description":"****",
            "price":20
        }

        self.client.post(
            "/api/v1/product",
            data=json.dumps(product_data),
            headers={"content-type":"application/json"}
        )
        return jsonify ({"message":"enter valid product description"})



def tearDown(self):
    self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
