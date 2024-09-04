# Shopping Cart Kata

This is a simple Flask-based shopping cart system.

## Features
- **CRUD operations for products**: Create, Read, Update, and Delete products from the pricing table.
- **Calculates subtotal with special pricing rules**: Includes support for special pricing (e.g., "3 for 140").
- **JSON-based API endpoints**: All operations are performed via JSON-based RESTful API endpoints.

## API Endpoints

### Pricing Endpoints

1. **POST /api/pricing**  
   **Description**: Replace the entire pricing table with a new set of products. This clears the existing table before inserting new products.  
   **Request Body**: JSON list of products, each containing:
   - `code` (string): Unique product code.
   - `unit_price` (float): Price per unit.
   - `special_price` (string, optional): Special price in the format `"x for y"` (e.g., "3 for 140").

   **Response**:  
   - Success: `201 Created` with a success message.
   - Error: `400 Bad Request` if the request format is incorrect or missing required fields.

2. **PUT /api/pricing**  
   **Description**: Update or add products in the pricing table. If a product with the given code exists, it will be updated; otherwise, it will be added.  
   **Request Body**: JSON list of products (same format as the POST request).  
   **Response**:  
   - Success: `200 OK` with a success message.
   - Error: `400 Bad Request` if the request format is incorrect or missing required fields.

3. **GET /api/pricing**  
   **Description**: Retrieve the entire pricing table.  
   **Response**:  
   - Success: `200 OK` with a list of all products in the pricing table.

4. **PATCH /api/pricing/<code>**  
   **Description**: Partially update a product's details by its code. Only the fields provided in the request body will be updated.  
   **Request Body**: JSON object with fields to update (e.g., `unit_price`, `special_price`).  
   **Response**:  
   - Success: `200 OK` with a success message.
   - Error: `404 Not Found` if the product with the given code does not exist.

### Subtotal Endpoint

1. **POST /api/subtotal**  
   **Description**: Calculate the subtotal based on a list of products and their quantities. Supports special pricing.  
   **Request Body**: JSON list of items, each containing:
   - `code` (string): The product code.
   - `quantity` (int): The quantity of the product to calculate the subtotal for.

   **Response**:  
   - Success: `200 OK` with the calculated subtotal.
   - Error: `400 Bad Request` if the request format is incorrect or required fields are missing.
   - Error: `404 Not Found` if a product code is not found.

## Running the Application

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The app will start in development mode, and you can access the API at `http://127.0.0.1:5000/`.

## Example Request

### Calculate Subtotal:
```bash
curl -X POST http://127.0.0.1:5000/api/subtotal -H "Content-Type: application/json" -d '[
    {"code": "A", "quantity": 3},
    {"code": "B", "quantity": 2}
]'
```

### Example Response:
```json
{
    "subtotal": 270
}
```

## Configuration

Configuration settings are managed in the `config.py` file, which includes database settings and other Flask configurations.

## Database Setup

This app uses Flask-Migrate for database migrations. To initialize the database, use the following commands:

```bash
flask db init
flask db migrate
flask db upgrade
```
## Run Unit Test

```bash
python -m unittest discover -s tests

python tests/test_app.py  #(a HTML report will be generated)
```