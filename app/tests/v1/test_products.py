import json
import unittest
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
        self.order_data = {
            "product": "Microphone",
            "category": "Electronics",
            "price": 2500
        }

    def test_get_specific_product(self):
        ''' Test to get single product '''

        neworder = self.client.post(
            "/api/v1/products",
            data=json.dumps(self.order_data),
            headers={"content-type": "application/json"}
        )
        response = self.client.get(
            "/api/v1/products/1", content_type='application/json')

        self.assertEqual(response.content_type, 'application/json')
        print(neworder, response)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

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

        response = self.client.post(
            "/api/v1/product",
            data=json.dumps(self.order_data),
            headers={"content-type":"application/json"}
        )

        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'], "record created")

class Testsales(TestCase):
    '''Test the sales'''

    def setUp(self):
        """Define test variables and create an istance of a record"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.record_data = {
            "product": "Microphone",
            "category": "Electronics",
            "price per unit": 2500,
            "quantity sold": 20,
        }

    def test_create_new_sale_record(self):
        ''' Test to write new sale record '''

        response = self.client.post(
            "/api/v1/salerecord",
            data=json.dumps(self.record_data),
            headers={"content-type": "application/json"}
        )

        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'], "record created")

    def test_get_all_records(self):
        ''' Test to get all records '''

        response = self.client.get(
            "/api/v1/salerecords", content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)


def tearDown(self):
    self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
