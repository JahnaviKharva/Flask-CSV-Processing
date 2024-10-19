import os
from datetime import timedelta
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Set to 1 hour

    # Database configuration
    DB_HOST = os.getenv('DATABASE_HOST')  # No fallback needed
    DB_NAME = os.getenv('DATABASE_NAME')
    DB_USER = os.getenv('DATABASE_USER')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
    DB_PORT = int(os.getenv('DATABASE_PORT'))


class DevelopmentConfig(Config):
    """Development configuration settings."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration settings."""
    DEBUG = False
