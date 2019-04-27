# api/github/config.py
import os

DB_NAME = os.environ.get("DB_NAME", "")
DB_URL = os.environ.get("DB_URL", "")

class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    MONGODB_SETTINGS = {
        "db": DB_NAME,
        "host": DB_URL
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    """Production configuration"""
    MONGO_DATABASE_URI = os.environ.get("DATABASE_URL")
