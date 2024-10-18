import os
from datetime import timedelta

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Set to 1 hour

    # Database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'purchase_db')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Janu@123')
    DB_PORT = os.environ.get('DB_PORT', 5432)


class DevelopmentConfig(Config):
    """Development configuration settings."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration settings."""
    DEBUG = False
