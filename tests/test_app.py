import sys
import os
# Add the project root directory to sys.path before importing app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import HtmlTestRunner
from app import app


class ShoppingCartTestCase(unittest.TestCase):

    def setUp(self):
        # Setup for testing using Flask's test_client
        self.app = app.test_client()
        self.app.testing = True

    # Test subtotal calculation
    def test_subtotal(self):
        # Ensure products are added before subtotal calculation
        self.app.post('/api/pricing', json=[
            {"code": "A", "unit_price": 50, "special_price": "3 for 140"},
            {"code": "B", "unit_price": 35, "special_price": "2 for 60"},
            {"code": "C", "unit_price": 25, "special_price": None},
            {"code": "D", "unit_price": 12, "special_price": None}
        ])

        # Simulate a list of items with product codes and quantities
        response = self.app.post('/api/subtotal', json=[
            {"code": "A", "quantity": 3},
            {"code": "B", "quantity": 3},
            {"code": "C", "quantity": 1},
            {"code": "D", "quantity": 2}
        ])
        data = response.get_json()

        # Check if the subtotal is correctly calculated
        self.assertEqual(data['subtotal'], 284)

    # Test getting the pricing table
    def test_get_pricing_table(self):
        # # Ensure products exist
        self.app.post('/api/pricing', json=[
            {"code": "A", "unit_price": 50, "special_price": "3 for 140"},
            {"code": "B", "unit_price": 35, "special_price": "2 for 60"},
            {"code": "C", "unit_price": 25, "special_price": None},
            {"code": "D", "unit_price": 12, "special_price": None}
        ])

        response = self.app.get('/api/pricing')
        data = response.get_json()

        # Check if some known products are in the pricing table
        self.assertIsInstance(data, list)
        products = [product['code'] for product in data]
        self.assertIn('A', products)
        self.assertIn('B', products)

    # Test adding a product to the pricing table
    def test_add_product(self):
        # Add a new product
        response = self.app.put('/api/pricing', json=[
            {"code": "E", "unit_price": 20, "special_price": None}
        ])  # Change to PUT to add product without replacing table
        data = response.get_json()

        # Verify the success message
        self.assertEqual(data['message'], 'Pricing table updated successfully')

        # Confirm the product exists in the pricing table
        response = self.app.get('/api/pricing')
        data = response.get_json()
        products = [product['code'] for product in data]
        self.assertIn('E', products)

    # Test updating an existing product in the pricing table
    def test_update_product(self):
        # Update the product's unit_price and special_price
        response = self.app.put('/api/pricing', json=[
            {"code": "A", "unit_price": 55, "special_price": "3 for 150"}
        ])
        data = response.get_json()

        # Verify the success message
        self.assertEqual(data['message'], 'Pricing table updated successfully')

        # Confirm the product has been updated correctly
        response = self.app.get('/api/pricing')
        data = response.get_json()
        product_a = next(product for product in data if product['code'] == 'A')
        self.assertEqual(product_a['unit_price'], 55)
        self.assertEqual(product_a['special_price'], '3 for 150')

    # Test partial update of an existing product
    def test_partial_update_product(self):
        # Update the product's special_price only
        response = self.app.patch('/api/pricing/A', json={"special_price": "3 for 160"})
        data = response.get_json()

        # Verify the success message
        self.assertEqual(data['message'], 'Product A updated successfully')

        # Confirm the product has been partially updated
        response = self.app.get('/api/pricing')
        data = response.get_json()
        product_a = next(product for product in data if product['code'] == 'A')
        self.assertEqual(product_a['special_price'], '3 for 160')

    # Test for invalid special price format
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
