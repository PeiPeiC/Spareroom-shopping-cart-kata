import os
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file automatically
class Config:
    # General Flask Config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
