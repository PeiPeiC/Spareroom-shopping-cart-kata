# Shopping Cart Kata

This is a simple Flask-based shopping cart system.

## Features
- CRUD operations for products.
- Calculates subtotal with special pricing rules.
- JSON-based API endpoints.

## API Endpoints

- `POST /api/subtotal` - Calculate the subtotal for the given items.
- `GET /api/pricing` - Retrieve the pricing table.
- `POST /api/pricing` - Add a new product.
- `PUT /api/pricing/<code>` - Update product pricing.

## Running the Application

1. Install dependencies:

```sh
pip install -r requirements.txt
