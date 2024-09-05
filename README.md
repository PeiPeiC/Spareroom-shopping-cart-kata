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

### Virtual Environment Setup

To set up a virtual environment in Python:

1. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/project
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**:
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
After the virtual envirnment is set up:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL**: Ensure that PostgreSQL is running on your system and set in .env or add the herouku postgresql uri in .env

3. **Run the Flask application**:
   - **Mac OS**:
     ```bash
     export FLASK_APP=app.py
     ```
   - **Windows**:
     ```bash
     set FLASK_APP=app.py
     ```

4. **Start the Flask app**:
   ```bash
   python app.py
   ```
   or
   ```bash
   flask run
   ```

   The app will start in development mode, and you can access the API at `http://127.0.0.1:5000/`.



4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Deactivate the virtual environment** when you're done:
   ```bash
   deactivate
   ```

## Database Setup

This app uses Flask-Migrate for database migrations. To initialize the database:

1. **Initialize the database**:
   ```bash
   flask db init
   ```

2. **Create a migration**:
   ```bash
   flask db migrate
   ```

3. **Apply the migration**:
   ```bash
   flask db upgrade
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
