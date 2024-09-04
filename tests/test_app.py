from unittest.mock import patch, MagicMock
import unittest
import HtmlTestRunner
import sys
import os

# Add the project root directory to sys.path before importing app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from model import Product


class ShoppingCartTestCase(unittest.TestCase):

    def setUp(self):
        # Setup Flask's test_client and push the application context
        self.app = app.test_client()
        self.app.testing = True
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        # Pop the application context after each test
        self.ctx.pop()

    # Mock the commit and query methods for database session
    @patch('app.db.session.commit')
    @patch('app.db.session.add')
    @patch('app.db.session.query')  # Mock query
    def test_subtotal(self, mock_query, mock_add, mock_commit):
        # Create mock products as per the pricing dataset
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.code = 'A'
        mock_product_A.unit_price = 50
        mock_product_A.special_price = '3 for 140'  # Ensure mock uses '3 for 140'

        mock_product_B = MagicMock(spec=Product)
        mock_product_B.code = 'B'
        mock_product_B.unit_price = 35
        mock_product_B.special_price = '2 for 60'

        mock_product_C = MagicMock(spec=Product)
        mock_product_C.code = 'C'
        mock_product_C.unit_price = 25
        mock_product_C.special_price = None

        mock_product_D = MagicMock(spec=Product)
        mock_product_D.code = 'D'
        mock_product_D.unit_price = 12
        mock_product_D.special_price = None

        # Mock the session query to return the correct product based on the code
        def filter_by_code(code):
            if code == 'A':
                return mock_product_A
            elif code == 'B':
                return mock_product_B
            elif code == 'C':
                return mock_product_C
            elif code == 'D':
                return mock_product_D
            else:
                return None

        # Mock the filter_by method to use filter_by_code
        mock_query.filter_by.side_effect = lambda **kwargs: MagicMock(first=lambda: filter_by_code(kwargs['code']))

        # Send request for subtotal calculation
        response = self.app.post('/api/subtotal', json=[
            {"code": "A", "quantity": 3},
            {"code": "B", "quantity": 3},
            {"code": "C", "quantity": 1},
            {"code": "D", "quantity": 2}
        ])

        data = response.get_json()

        # Verify the subtotal calculation based on mock pricing dataset
        expected_subtotal = 140 + 60 + 35 + 25 + (2 * 12)  # 140 + 95 + 25 + 24 = 284
        self.assertEqual(data['subtotal'], expected_subtotal)

    @patch('app.db.session.commit')
    @patch('app.db.session.add')
    @patch('app.db.session.query')
    def test_get_pricing_table(self, mock_query, mock_add, mock_commit):
        # Mock the query to return a list of Product objects
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.code = 'A'
        mock_product_A.unit_price = 50
        mock_product_A.special_price = '3 for 140'

        mock_product_B = MagicMock(spec=Product)
        mock_product_B.code = 'B'
        mock_product_B.unit_price = 35
        mock_product_B.special_price = '2 for 60'

        mock_product_C = MagicMock(spec=Product)
        mock_product_C.code = 'C'
        mock_product_C.unit_price = 25
        mock_product_C.special_price = None

        mock_product_D = MagicMock(spec=Product)
        mock_product_D.code = 'D'
        mock_product_D.unit_price = 12
        mock_product_D.special_price = None

        # Mock the session query to return the mocked products
        mock_query.return_value.all.return_value = [mock_product_A, mock_product_B, mock_product_C, mock_product_D]

        response = self.app.get('/api/pricing')
        data = response.get_json()

        # Check if some known products are in the pricing table
        self.assertIsInstance(data, list)
        products = [product['code'] for product in data]
        self.assertIn('A', products)
        self.assertIn('B', products)
        self.assertIn('C', products)
        self.assertIn('D', products)

    @patch('app.db.session.commit')
    @patch('app.db.session.add')
    def test_add_product(self, mock_add, mock_commit):
        # Add a new product
        response = self.app.put('/api/pricing', json=[
            {"code": "E", "unit_price": 20, "special_price": None}
        ])
        mock_commit.assert_called_once()  # Ensure commit is called
        mock_add.assert_called_once()  # Ensure add was called once

        # Verify the success message
        data = response.get_json()
        self.assertEqual(data['message'], 'Pricing table updated successfully')

    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_update_product(self, mock_query, mock_commit):
        # Update the product's unit_price and special_price
        response = self.app.put('/api/pricing', json=[
            {"code": "A", "unit_price": 55, "special_price": "3 for 150"}
        ])
        mock_commit.assert_called_once()  # Ensure commit is called

        # Mock the updated product A
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.code = 'A'
        mock_product_A.unit_price = 55
        mock_product_A.special_price = '3 for 150'

        # Mock the session query to return the updated product
        mock_query.return_value.all.return_value = [mock_product_A]

        # Verify the success message
        data = response.get_json()
        self.assertEqual(data['message'], 'Pricing table updated successfully')

    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_partial_update_product(self, mock_query, mock_commit):
        # Update the product's special_price only
        response = self.app.patch('/api/pricing/A', json={"special_price": "3 for 160"})
        mock_commit.assert_called_once()  # Ensure commit is called

        # Mock the updated product A
        mock_product_A = MagicMock(spec=Product)
        mock_product_A.code = 'A'
        mock_product_A.special_price = '3 for 160'

        # Mock the session query to return the updated product
        mock_query.return_value.all.return_value = [mock_product_A]

        # Verify the success message
        data = response.get_json()
        self.assertEqual(data['message'], 'Product A updated successfully')

    def test_invalid_special_price(self):
        # Attempt to update with an invalid special price format
        response = self.app.put('/api/pricing', json=[
            {"code": "A", "special_price": "3 for x"}
        ])
        data = response.get_json()

        # Check for an error message
        self.assertIn('error', data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_reports'))
