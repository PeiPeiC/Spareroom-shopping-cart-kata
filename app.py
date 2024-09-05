from flask import Flask, request, jsonify
from flask_migrate import Migrate
from config import Config
from model import db, Product
import re
from flask import current_app
import logging

def create_app(config_class=Config):
    # Create Flask app using factory pattern
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the database and migration tool
    db.init_app(app)
    migrate = Migrate(app, db)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Define routes within the app factory
    @app.route('/api/pricing', methods=['POST'])
    def replace_pricing_table():
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format. Expecting a list of products."}), 400
        Product.query.delete()
        for product_data in data:
            code = product_data.get('code')
            unit_price = product_data.get('unit_price')
            special_price = product_data.get('special_price')
            if not code or not unit_price:
                return jsonify({"error": f"Missing code or unit price for product: {product_data}"}), 400
            new_product = Product(code=code, unit_price=unit_price, special_price=special_price)
            db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Pricing table replaced successfully"}), 201

    @app.route('/api/pricing', methods=['PUT'])
    def update_pricing_table():
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid data format. Expecting a list of products."}), 400
        for product_data in data:
            code = product_data.get('code')
            unit_price = product_data.get('unit_price')
            special_price = product_data.get('special_price')
            if not code or not unit_price:
                return jsonify({"error": f"Missing code or unit price for product: {product_data}"}), 400
            product = Product.query.filter_by(code=code).first()
            if product:
                product.unit_price = unit_price
                product.special_price = special_price
            else:
                new_product = Product(code=code, unit_price=unit_price, special_price=special_price)
                db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Pricing table updated successfully"}), 200

    @app.route('/api/pricing', methods=['GET'])
    def get_pricing_table():
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])

    @app.route('/api/pricing/<code>', methods=['PATCH'])
    def update_product_partially(code):
        product = Product.query.filter_by(code=code).first()
        if not product:
            return jsonify({"error": f"Product with code {code} not found"}), 404
        data = request.json
        if 'unit_price' in data:
            product.unit_price = data['unit_price']
        if 'special_price' in data:
            product.special_price = data['special_price']
        db.session.commit()
        return jsonify({"message": f"Product {code} updated successfully"}), 200

    @app.route('/api/pricing', methods=['DELETE'])
    def delete_products():
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Invalid input format. Expected a list of product codes."}), 400

        deleted_products = []
        for code in data:
            product = Product.query.filter_by(code=code).first()
            if product:
                db.session.delete(product)
                deleted_products.append(code)
            else:
                current_app.logger.warning(f"Product with code {code} not found.")
        
        if deleted_products:
            db.session.commit()
            return jsonify({"message": "Products deleted successfully", "deleted_products": deleted_products}), 200
        else:
            return jsonify({"error": "No products found to delete."}), 404

    @app.route('/api/subtotal', methods=['POST'])
    def calculate_subtotal():
        try:
            items = request.json
            total = 0
            if not isinstance(items, list):
                return jsonify({'error': 'Invalid input format. Expected a list of items.'}), 400
            for item in items:
                code = item.get('code')
                quantity = item.get('quantity')
                if not code or not quantity:
                    return jsonify({'error': f'Missing code or quantity for item: {item}'}), 400
                product = Product.query.filter_by(code=code).first()
                if not product:
                    current_app.logger.error(f"Product with code {code} not found.")
                    return jsonify({'error': f'Product with code {code} not found.'}), 404
                item_total = _calculate_item_total(product.unit_price, product.special_price, quantity)
                if item_total == -1:
                    return jsonify({'error': f'Error calculating total for item {code}.'}), 400
                total += item_total
            return jsonify({'subtotal': total})
        except Exception as e:
            current_app.logger.error(f"Error calculating subtotal: {str(e)}")
            return jsonify({'error': 'Internal server error. Please try again later.'}), 500

    def _calculate_item_total(unit_price, special_price, quantity):
        try:
            if special_price:
                match = re.match(r'(\d+) for (\d+)', special_price)
                if match:
                    count = int(match.group(1))
                    special_price_value = int(match.group(2))
                    total_special = (quantity // count) * special_price_value
                    total_regular = (quantity % count) * unit_price
                    return total_special + total_regular
            return unit_price * quantity
        except Exception as e:
            current_app.logger.error(f"Error calculating item total: {str(e)}")
            return -1

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
