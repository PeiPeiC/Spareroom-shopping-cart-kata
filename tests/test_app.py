import sys
import os

# add the root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import HtmlTestRunner
from unittest.mock import patch, MagicMock
from app import create_app
from model import Product, db

class ShoppingCartTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def setUp(self):
        # set up app context
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # clear app context
        self.app_context.pop()

    @patch('model.Product.query')
    def test_get_pricing_table(self, mock_query):
        # mock products data
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.to_dict.return_value = {"code": "A", "unit_price": 50, "special_price": "3 for 140"}

        mock_product_B = MagicMock(spec=Product)
        mock_product_B.to_dict.return_value = {"code": "B", "unit_price": 35, "special_price": "2 for 60"}

        # mock query results
        mock_query.all.return_value = [mock_product_A, mock_product_B]

        # get pricing table        
        response = self.client.get('/api/pricing')
        data = response.get_json()

        # validate response
        self.assertEqual(len(data), 2)
        self.assertIn('A', [product['code'] for product in data])
        self.assertIn('B', [product['code'] for product in data])

    @patch('model.Product.query')
    def test_subtotal(self, mock_query):
        # mock products data
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.unit_price = 50
        mock_product_A.special_price = "3 for 140"

        mock_product_B = MagicMock(spec=Product)
        mock_product_B.unit_price = 35
        mock_product_B.special_price = "2 for 60"

        mock_product_C = MagicMock(spec=Product)
        mock_product_C.unit_price = 25
        mock_product_C.special_price = None

        mock_product_D = MagicMock(spec=Product)
        mock_product_D.unit_price = 12
        mock_product_D.special_price = None

        # 模拟查询结果
        def filter_by_code(code):
            return {
                'A': mock_product_A,
                'B': mock_product_B,
                'C': mock_product_C,
                'D': mock_product_D
            }.get(code, None)

        # Mock `filter_by` 和 `first`
        mock_query.filter_by.side_effect = lambda **kwargs: MagicMock(first=lambda: filter_by_code(kwargs['code']))

        # test subtotal calculation
        response = self.client.post('/api/subtotal', json=[
            {"code": "A", "quantity": 3},
            {"code": "B", "quantity": 3},
            {"code": "C", "quantity": 1},
            {"code": "D", "quantity": 2}
        ])

        data = response.get_json()

        # check subtotal calculation
        expected_subtotal = 140 + 60 + 35 + 25 + (2 * 12)  # 284
        self.assertIn('subtotal', data)
        self.assertEqual(data['subtotal'], expected_subtotal)

    @patch('model.Product.query')
    def test_post_pricing_and_subtotal(self, mock_query):
        # mock products data
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.unit_price = 40
        mock_product_A.special_price = "3 for 100"

        mock_product_B = MagicMock(spec=Product)
        mock_product_B.unit_price = 60
        mock_product_B.special_price = "2 for 60"

        mock_product_C = MagicMock(spec=Product)
        mock_product_C.unit_price = 77
        mock_product_C.special_price = None

        mock_product_D = MagicMock(spec=Product)
        mock_product_D.unit_price = 66
        mock_product_D.special_price = None

        # mock query results
        def filter_by_code(code):
            return {
                'A': mock_product_A,
                'B': mock_product_B,
                'C': mock_product_C,
                'D': mock_product_D
            }.get(code, None)

        # Mock `filter_by` 和 `first`
        mock_query.filter_by.side_effect = lambda **kwargs: MagicMock(first=lambda: filter_by_code(kwargs['code']))

        # mock data to prevent database access
        response = self.client.post('/api/subtotal', json=[
            {"code": "A", "quantity": 3},
            {"code": "B", "quantity": 3},
            {"code": "C", "quantity": 1},
            {"code": "D", "quantity": 2}
        ])

        data = response.get_json()


        #check subtotal calculation
        expected_subtotal = 100 + 60 + 60 + 77 + (2 * 66)  # 429
        self.assertIn('subtotal', data)
        self.assertEqual(data['subtotal'], expected_subtotal)

    @patch('model.Product.query')
    @patch('model.db.session.commit')
    @patch('model.db.session.add')
    def test_put_pricing_table(self, mock_add, mock_commit, mock_query):
        # Mock existing products
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.code = 'A'
        mock_product_B = MagicMock(spec=Product)
        mock_product_B.code = 'B'

        # Mock query result for existing product A
        mock_query.filter_by.side_effect = lambda code: MagicMock(first=lambda: mock_product_A if code == 'A' else None)

        # Send PUT request to update pricing table
        response = self.client.put('/api/pricing', json=[
            {"code": "A", "unit_price": 55, "special_price": "3 for 145"},
            {"code": "B", "unit_price": 35, "special_price": "2 for 65"}
        ])

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Pricing table updated successfully')

        # Verify that session.add() was called once for product B (since it's new)
        mock_add.assert_called_once()

        # Verify that session.commit() was called
        mock_commit.assert_called_once()

    @patch('model.Product.query')
    @patch('model.db.session.commit')
    def test_patch_product(self, mock_commit, mock_query):
        # Mock existing product
        mock_product = MagicMock(spec=Product)
        mock_product.code = 'A'
        mock_product.unit_price = 50
        mock_product.special_price = '3 for 140'

        # Mock query result for product A
        mock_query.filter_by.side_effect = lambda code: MagicMock(first=lambda: mock_product)

        # Send PATCH request to update product A partially
        response = self.client.patch('/api/pricing/A', json={"special_price": "3 for 150"})

        data = response.get_json()

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Product A updated successfully')

        # Verify that product's special price was updated
        self.assertEqual(mock_product.special_price, '3 for 150')

        # Verify that session.commit() was called
        mock_commit.assert_called_once()

    @patch('model.Product.query')
    @patch('model.db.session.delete')
    @patch('model.db.session.commit')
    def test_delete_products(self, mock_commit, mock_delete, mock_query):
        # Mock products data
        mock_product_A = MagicMock(spec=Product)
        mock_product_B = MagicMock(spec=Product)

        # Mock query results for products to delete
        def filter_by_code(code):
            return {
                'A': mock_product_A,
                'B': mock_product_B
            }.get(code, None)

        # Mock `filter_by` 和 `first`
        mock_query.filter_by.side_effect = lambda **kwargs: MagicMock(first=lambda: filter_by_code(kwargs['code']))

        # Send request to delete products
        response = self.client.delete('/api/pricing', json=['A', 'B'])

        data = response.get_json()

        # Verify products were deleted and committed
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('deleted_products', data)
        self.assertEqual(data['deleted_products'], ['A', 'B'])

        # Verify delete and commit were called
        self.assertEqual(mock_delete.call_count, 2)  # Two products deleted
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_reports'))
