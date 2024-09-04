from flask import Flask, request, jsonify
from flask_migrate import Migrate
from config import Config
from model import db, Product
import re
from flask import current_app

# Initialize the Flask app
app = Flask(__name__)

# Load config settings from the Config class
app.config.from_object(Config)

# Initialize the database and migration tool
db.init_app(app)
migrate = Migrate(app, db)

# Routes

# POST: Replace the entire pricing table with new data
@app.route('/api/pricing', methods=['POST'])
def replace_pricing_table():
    """
    Replaces the entire product pricing table with a new set of products.
    Clears the existing table and inserts the new products provided in the request body.
    """
    data = request.json  # Expecting a list of products

    # Ensure that the request contains a list of products
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format. Expecting a list of products."}), 400

    # Clear the entire table (delete all existing products)
    Product.query.delete()

    # Add new products to the now-empty table
    for product_data in data:
        code = product_data.get('code')
        unit_price = product_data.get('unit_price')
        special_price = product_data.get('special_price')

        # Validate that each product has a code and unit price
        if not code or not unit_price:
            return jsonify({"error": f"Missing code or unit price for product: {product_data}"}), 400

        # Create a new product and add it to the session
        new_product = Product(code=code, unit_price=unit_price, special_price=special_price)
        db.session.add(new_product)

    # Commit the transaction for all added products
    db.session.commit()

    return jsonify({"message": "Pricing table replaced successfully"}), 201


# PUT: Update the pricing table, either adding new products or updating existing ones
@app.route('/api/pricing', methods=['PUT'])
def update_pricing_table():
    """
    Updates the product pricing table. 
    One or more products can be added or updated in the table.
    If a product with the given code exists, 
    it will update the product. If the product does not exist, it will be added.
    """
    data = request.json  # Expecting a list of products

    # Ensure that the request contains a list of products
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format. Expecting a list of products."}), 400

    # Update or add each product in the list
    for product_data in data:
        code = product_data.get('code')
        unit_price = product_data.get('unit_price')
        special_price = product_data.get('special_price')

        # Validate that each product has a code and unit price
        if not code or not unit_price:
            return jsonify({"error": f"Missing code or unit price for product: {product_data}"}), 400

        # Check if product already exists
        product = Product.query.filter_by(code=code).first()

        if product:
            # Update existing product
            product.unit_price = unit_price
            product.special_price = special_price
        else:
            # Add new product if it doesn't exist
            new_product = Product(code=code, unit_price=unit_price, special_price=special_price)
            db.session.add(new_product)

    # Commit the changes for all products
    db.session.commit()

    return jsonify({"message": "Pricing table updated successfully"}), 200


# GET: Retrieve the entire pricing table
@app.route('/api/pricing', methods=['GET'])
def get_pricing_table():
    """
    Retrieves and returns all products from the pricing table.
    """
    products = Product.query.all()  # Fetch all products from the database
    return jsonify([product.to_dict() for product in products])  # Return product data as JSON


# PATCH: Update a single product partially based on its code
@app.route('/api/pricing/<code>', methods=['PATCH'])
def update_product_partially(code):
    """
    Partially updates the details of a single product by its code.
    Only the fields provided in the request body will be updated.
    """
    # Find the product by its code
    product = Product.query.filter_by(code=code).first()

    if not product:
        return jsonify({"error": f"Product with code {code} not found"}), 404

    # Get the fields to update from the request
    data = request.json

    # Update fields if present in the request body
    if 'unit_price' in data:
        product.unit_price = data['unit_price']
    
    if 'special_price' in data:
        product.special_price = data['special_price']

    # Commit the changes
    db.session.commit()
        
    return jsonify({"message": f"Product {code} updated successfully"}), 200



# POST: Calculate the subtotal based on a list of items
@app.route('/api/subtotal', methods=['POST'])
def calculate_subtotal():
    """
    Calculates the subtotal based on a list of products and quantities provided 
    in the request body. Returns a descriptive error message if any error occurs.
    """
    try:
        items = request.json  # Expecting a list of items
        total = 0  # Initialize total to 0

        # Ensure that 'items' is a list
        if not isinstance(items, list):
            return jsonify({'error': 'Invalid input format. Expected a list of items.'}), 400

        # Loop through each item in the list
        for item in items:
            code = item.get('code')
            quantity = item.get('quantity')

            # Skip items with missing code or quantity
            if not code or not quantity:
                return jsonify({'error': f'Missing code or quantity for item: {item}'}), 400

            # Find the product by its item code
            product = Product.query.filter_by(code=code).first()

            if not product:
                # If the product is not found, return an error message
                app.logger.error(f"Product with code {code} not found.")
                return jsonify({'error': f'Product with code {code} not found.'}), 404

            # Calculate the subtotal for this product
            item_total = _calculate_item_total(product.unit_price, product.special_price, quantity)

            # If there's an error in calculating item total, return a detailed error message
            if item_total == -1:
                return jsonify({'error': f'Error calculating total for item {code}.'}), 400

            total += item_total

        # Return the total as JSON
        return jsonify({'subtotal': total})

    except Exception as e:
        # Log any unexpected errors and return a generic error message
        app.logger.error(f"Error calculating subtotal: {str(e)}")
        return jsonify({'error': 'Internal server error. Please try again later.'}), 500



def _calculate_item_total(unit_price, special_price, quantity):
    """
    Helper function to calculate the total cost for a product based on the 
    quantity and special price (if any). Returns -1 if any error occurs.
    """
    try:
        if special_price:
            # Parse the special price format (e.g., "3 for 140")
            match = re.match(r'(\d+) for (\d+)', special_price)
            if match:
                count = int(match.group(1))
                special_price_value = int(match.group(2))
                # Calculate total for special price items
                total_special = (quantity // count) * special_price_value
                # Calculate total for remaining regular price items
                total_regular = (quantity % count) * unit_price
                return total_special + total_regular
        # If no special price, return total based on unit price
        return unit_price * quantity
    except Exception as e:
        # Log errors in the item calculation
        app.logger.error(f"Error calculating item total: {str(e)}")
        return -1  # Return -1 in case of error



# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
