import re

class PricingTable:
    def __init__(self):
        self.table = {
            "A": {"unit_price": 50, "special_price": "3 for 140"},
            "B": {"unit_price": 35, "special_price": "2 for 60"},
            "C": {"unit_price": 25, "special_price": None},
            "D": {"unit_price": 12, "special_price": None}
        }

    def get_table(self):
        return self.table

    def add_product(self, product):
        code = product['code']
        unit_price = product['unit_price']
        special_price = product.get('special_price', None)

        if special_price:
            self._validate_special_price(special_price)

        self.table[code] = {
            'unit_price': unit_price,
            'special_price': special_price
        }

    def update_product(self, code, updates):
        if code not in self.table:
            raise ValueError("Product not found")

        if 'unit_price' in updates:
            self.table[code]['unit_price'] = updates['unit_price']

        if 'special_price' in updates:
            self._validate_special_price(updates['special_price'])
            self.table[code]['special_price'] = updates['special_price']

    def calculate_subtotal(self, items):
        total = 0
        for item in items:
            code = item['code']
            quantity = item['quantity']
            if code in self.table:
                product = self.table[code]
                unit_price = product['unit_price']
                special_price = product['special_price']
                total += self._calculate_item_total(unit_price, special_price, quantity)
        return total

    def _calculate_item_total(self, unit_price, special_price, quantity):
        if special_price:
            match = re.match(r'(\d+) for (\d+)', special_price)
            if match:
                count = int(match.group(1))
                special_price_value = int(match.group(2))
                total_special = (quantity // count) * special_price_value
                total_regular = (quantity % count) * unit_price
                return total_special + total_regular
        return unit_price * quantity

    def _validate_special_price(self, special_price):
        if not re.match(r'^\d+ for \d+$', special_price):
            raise ValueError("Special price format must be '__ for __'")
