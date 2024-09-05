# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable (You can add others, like SQLALCHEMY_DATABASE_URI, if needed)
ENV FLASK_ENV=development

# Run the application using python instead of flask run
CMD ["python", "app.py"]
