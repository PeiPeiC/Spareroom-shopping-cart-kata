### Docker commands

1. **Starting and Building Containers**:
    ```bash
    docker-compose up --build
    ```
    - This command builds and starts the containers defined in your `docker-compose.yml` file.
    - The `--build` flag ensures that the images are rebuilt before starting the containers. This is useful if you've made changes to the Dockerfile or other parts of your application since the last time the containers were built.

2. **Viewing Application Logs**:
    ```bash
    docker-compose logs app
    ```
    - This command shows the logs for the container named `app`. You can monitor what’s happening inside your application, such as errors or other log messages.
    - It helps to diagnose issues during the container's operation.

3. **Checking Running Containers**:
    ```bash
    docker ps
    ```
    - This command lists all the running Docker containers. You’ll see container IDs, names, ports, and other essential information.
    - It helps to verify that your containers are running correctly.

4. **Stopping and Removing Containers**:
    ```bash
    docker-compose down
    ```
    - This command stops and removes all the containers, networks, and volumes defined in your `docker-compose.yml` file.
    - Use this when you want to fully stop and clean up your Docker environment.

5. **Applying Database Migrations**:
    ```bash
    docker-compose exec app flask db upgrade
    ```
    - This command runs a database migration using Flask’s migration tool inside the `app` container.
    - It applies any pending migrations to your database, ensuring your database schema is up to date with the latest changes.

6. **Accessing the Database Container**:
    ```bash
    docker-compose exec db bash
    ```
    - This command opens an interactive shell (bash) inside the `db` container. From here, you can directly interact with the database container.
    - It’s useful for manually inspecting or troubleshooting your PostgreSQL database.

### Verifying Database Migration

1. **Connecting to the Database from Inside the Container**:
    - After you are inside the `db` container (from the previous step), you can connect to the PostgreSQL database using the `psql` command:
    ```bash
    psql -h localhost -p 5432 -U username -d dbname
    ```
    or
    ```bash
    psql -U username -d dbname
    ```
    - This connects to the PostgreSQL server running inside the container. `-U` specifies the username, and `-d` specifies the database name.

2. **Checking for Tables**:
    ```bash
    \dt
    ```
    - This command lists all the tables in the current database once you’re connected via `psql`.
    - Use this to verify whether the migration successfully applied and created or altered the necessary tables.

3. **Directly Accessing the App Container**:
    ```bash
    docker exec -it spareroom-shopping-cart-kata-app-1 bash
    ```
    - This opens an interactive shell inside the `app` container (replace `spareroom-shopping-cart-kata-app-1` with your actual container name if it differs).
    - You can run various commands from within the container, useful for debugging or testing directly in the application environment.

### API Testing

1. **Testing API with `GET` Request**:
    ```bash
    curl -X GET http://127.0.0.1:5000/api/pricing
    ```
    - This sends a `GET` request to the `/api/pricing` endpoint of your Flask app, which is running on `http://127.0.0.1:5000`.
    - The `GET` method retrieves pricing data from your API.

    **For PowerShell**:
    ```bash
    Invoke-RestMethod -Uri http://127.0.0.1:5000/api/pricing -Method GET
    ```
    - In PowerShell, the `curl` command is actually an alias for `Invoke-WebRequest`, which doesn’t work the same way as in Unix-based systems. You should use `Invoke-RestMethod` instead to send API requests.

2. **Testing API with `POST` Request**:
    ```bash
    curl -X POST http://127.0.0.1:5000/api/pricing \
        -H "Content-Type: application/json" \
        -d '[
              {"code": "A", "unit_price": 50, "special_price": "3 for 130"},
              {"code": "B", "unit_price": 30, "special_price": "2 for 45"}
            ]'
    ```
    - This sends a `POST` request to the `/api/pricing` endpoint, adding or updating the pricing information in your system.
    - The `-H "Content-Type: application/json"` header tells the server that the data is in JSON format.
    - The `-d` flag is followed by the data being sent, in this case, an array of products with their respective codes, prices, and special prices.

---

### Initialising the Containers with Predefined Tables and Data
- When you first run `docker-compose up --build`, if your app is set up correctly (e.g., using Flask-Migrate or another migration tool), the initial tables and data will be created automatically based on the migrations defined in your code.
- If the migrations have already been applied, the containers should start with the necessary tables and data intact. You can verify this by connecting to the PostgreSQL container and running `\dt` to see the tables or querying the tables directly.