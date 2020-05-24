import os
from dotenv import load_dotenv
import secrets


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
env_path = os.path.join(PROJECT_DIR, ".env")
load_dotenv(env_path, override=True)


class Config:
    POSTGRES = {
        "user": "postgres",
        "pw": "password",
        "db": "flask_ecommerce",
        "host": "localhost",
        "port": "5432",
    }
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL") % POSTGRES
    SECRET_KEY = str(secrets.token_hex(16))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USE_SMTP = True
    CSRF_ENABLE = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = False


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "bad_key"
