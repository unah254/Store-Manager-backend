import json
import unittest
from flask import jsonify
from unittest import TestCase
from app import create_app

from app.tests.v1.base_test import BaseTest
class TestProducts(BaseTest):
    '''Test the products'''

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

    # def test_add_new_products_as_admin(self):
    #     """ Test add product items """

    #     token = self.get_token_as_admin()

    #     response = self.client.post(
    #         "/api/v1/products",
    #         data=json.dumps(self.product_data),
    #         headers={"content-type": "application/json",
    #                  "Authorization": f'Bearer {token}'
    #                  }
    #     )
        
        
    #     self.assertEqual(response.status_code, 201)



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


class Testsales(BaseTest):
    '''Test the sales'''

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

        invalid_product_description = {
            "name": "Valipro",
            "description": "****",
            "price": 20
        }

        self.client.post(
            "/api/v1/product",
            data=json.dumps(invalid_product_description),
            headers={"content-type": "application/json"}
        )
        return jsonify({"message": "enter valid product description"})

    # def test_invalid_product_name(self):
    #     ''' Test invalid product description '''

    #     invalid_product_data = {
    #         "name": "****",
    #         "description": "suitable for podcast",
    #         "price": 20
    #     }

    #     response = self.client.post(
    #         "/api/v1/products",
    #         data=json.dumps(invalid_product_data),
    #         headers={
    #             "content-type": "application/json",
    #             # "Authorization": f'Bearer'{token}
    #         }
    #     )
    #     self.assertEqual(response.data, "enter valid product name", 400)
    #     print(response)

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
