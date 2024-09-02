from flask import Flask, request, jsonify
from data import PricingTable

app = Flask(__name__)
pricing_table = PricingTable()

@app.route('/api/subtotal', methods=['POST'])
def calculate_subtotal():
    items = request.json
    subtotal = pricing_table.calculate_subtotal(items)
    return jsonify({'subtotal': subtotal})

@app.route('/api/pricing', methods=['GET'])
def get_pricing_table():
    return jsonify(pricing_table.get_table())

@app.route('/api/pricing', methods=['POST'])
def add_product():
    data = request.json
    pricing_table.add_product(data)
    return jsonify({'message': 'Product added successfully'})

@app.route('/api/pricing/<code>', methods=['PUT'])
def update_product(code):
    data = request.json
    try:
        pricing_table.update_product(code, data)
        return jsonify({'message': 'Product updated successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
