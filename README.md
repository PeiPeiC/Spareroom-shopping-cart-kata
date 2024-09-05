# Shopping Cart Kata

This is a simple Flask-based shopping cart system.  
Python version: **3.12.4**

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
   **Example**
   ```json
   [
      {
         "code": "A",
         "unit_price": 50,
         "special_price": "3 for 130"
      },
      {
         "code": "B",
         "unit_price": 30,
         "special_price": "2 for 45"
      },
      {
         "code": "C",
         "unit_price": 20
      }
   ]
   ```
   **Response**:  
   - Success: `201 Created` with a success message.
   - Error: `400 Bad Request` if the request format is incorrect or missing required fields.

2. **PUT /api/pricing**  
   **Description**: Update or add products in the pricing table. If a product with the given code exists, it will be updated; otherwise, it will be added.  
   **Request Body**: JSON list of products (same format as the POST request).  
   **Example**
   ```json
   [
      {
         "code": "A",
         "unit_price": 55,
         "special_price": "3 for 130"
      },
      {
         "code": "D",
         "unit_price": 40
      }
   ]
   ```
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
   **Example**
   ```json
   {
      "unit_price": 25,
      "special_price": "5 for 100"
   }
   ```
   **Response**:  
   - Success: `200 OK` with a success message.
   - Error: `404 Not Found` if the product with the given code does not exist.

5. **DELETE /api/pricing**  
   **Description**: Delete specific products by their codes.  
   **Request Body**: JSON list of product codes to delete.  
   **Example**
   ```json
   [
      "A",
      "B"
   ]
   ```
   **Response**:  
   - Success: `200 OK` with a list of deleted products.
   - Error: `404 Not Found` if none of the provided products exist.

### Subtotal Endpoint

1. **POST /api/subtotal**  
   **Description**: Calculate the subtotal based on a list of products and their quantities. Supports special pricing.  
   **Request Body**: JSON list of items, each containing:
   - `code` (string): The product code.
   - `quantity` (int): The quantity of the product to calculate the subtotal for.
   **Example**
   ```json
   [
      {
         "code": "A",
         "quantity": 3
      },
      {
         "code": "B",
         "quantity": 2
      }
   ]
   ```
   **Response**:  
   - Success: `200 OK` with the calculated subtotal.
   - Error: `400 Bad Request` if the request format is incorrect or required fields are missing.
   - Error: `404 Not Found` if a product code is not found.

## Running the Application

### Local Setup

If you are running the app locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd spareroom-shopping-cart-kata
   ```
2. **Set up a virtual environment**:
   Only required for local development (not necessary for Docker or Heroku deployments):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up PostgreSQL**: Make sure PostgreSQL is running, and ensure the correct credentials are set in `.env` or environment variables.

5. **Run database migrations**:
   ```bash
   flask db upgrade
   ```
6. **Run the Flask application**:
   - **Mac OS**:
     ```bash
     export FLASK_APP=app.py
     ```
   - **Windows**:
     ```bash
     set FLASK_APP=app.py
     ```
   Start the application:
   ```bash
   python app.py
   ```
   This will run the app locally at `http://127.0.0.1:5000/`.

7. **API Testing Example**:

   To test the `/api/subtotal` endpoint locally:

   ```bash
   curl -X POST http://localhost:5000/api/subtotal \
   -H "Content-Type: application/json" \
   -d '[{"code":"A","quantity":3},{"code":"B","quantity":3},{"code":"C","quantity":1},{"code":"D","quantity":2}]'
   ```

### Docker Setup

Alternatively, you can run the app using Docker:

1. **Run the app using Docker Compose**:
   ```bash
   docker-compose up --build
   ```
2. **Access the app** at `http://127.0.0.1:5000`.

3. **API Testing Example (within container)**:

   To test the `/api/subtotal` endpoint inside Docker:

   ```bash
   curl -X POST http://localhost:5000/api/subtotal \
   -H "Content-Type: application/json" \
   -d '[{"code":"A","quantity":3},{"code":"B","quantity":3},{"code":"C","quantity":1},{"code":"D","quantity":2}]'
   ```
### Heroku Deployment

The app is already deployed on Heroku:

- **Heroku App URL**: [https://spareroom-shopping-cart-kata-bdd866b64262.herokuapp.com/](https://spareroom-shopping-cart-kata-bdd866b64262.herokuapp.com/)

1. **API Testing Example on Heroku**:

   To test the `/api/subtotal` endpoint on Heroku:

   ```bash
   curl -X POST https://spareroom-shopping-cart-kata-bdd866b64262.herokuapp.com/api/subtotal \
   -H "Content-Type: application/json" \
   -d '[{"code":"A","quantity":3},{"code":"B","quantity":3},{"code":"C","quantity":1},{"code":"D","quantity":2}]'
   ```
## Run Unit Tests

1. **Run unit tests**:
   ```bash
   python -m unittest discover -s tests
   ```
2. **Generate HTML report**:
   ```bash
   python tests/test_app.py
   ```