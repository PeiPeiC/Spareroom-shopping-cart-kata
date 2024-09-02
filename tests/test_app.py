import unittest
from app import app

class ShoppingCartTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_subtotal(self):
        response = self.app.post('/api/subtotal', json=[{"code":"A","quantity":3},{"code":"B","quantity":3},{"code":"C","quantity":1},{"code":"D","quantity":2}])
        data = response.get_json()
        self.assertEqual(data['subtotal'], 284)

    def test_get_pricing_table(self):
        response = self.app.get('/api/pricing')
        data = response.get_json()
        self.assertIn('A', data)
        self.assertIn('B', data)

    def test_add_product(self):
        response = self.app.post('/api/pricing', json={"code":"E","unit_price":20})
        data = response.get_json()
        self.assertEqual(data['message'], 'Product added successfully')

    def test_update_product(self):
        response = self.app.put('/api/pricing/A', json={"unit_price":55, "special_price":"3 for 150"})
        data = response.get_json()
        self.assertEqual(data['message'], 'Product updated successfully')

    def test_invalid_special_price(self):
        response = self.app.put('/api/pricing/A', json={"special_price":"3 for x"})
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
