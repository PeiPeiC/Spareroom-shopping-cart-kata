To set up a virtual environment in Python:

1. **Navigate to your project directory:**

   ```bash
   cd /path/to/your/project
   ```

2. **Create a virtual environment:**

   If you're using Python 3, you can create a virtual environment with:

   ```bash
   python3 -m venv .venv
   ```

   This will create a virtual environment in a directory named `venv`.

3. **Activate the virtual environment:**

   - On **macOS/Linux**:

     ```bash
     source .venv/bin/activate
     ```

   - On **Windows**:

     ```bash
     .venv\Scripts\activate
     ```

   After activation, you should see `(venv)` at the beginning of your command prompt, indicating that the virtual environment is active.

4. **Install dependencies:**

   With the virtual environment activated, you can install the necessary dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

5. **Deactivate the virtual environment:**

   When you're done working in the virtual environment, you can deactivate it with:

   ```bash
   deactivate
   ```

This will return your shell to the global Python environment.