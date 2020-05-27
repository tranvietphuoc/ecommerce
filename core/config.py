import os
from dotenv import load_dotenv
import secrets


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
env_path = os.path.join(PROJECT_DIR, ".env")
load_dotenv(env_path, override=True)


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = str(secrets.token_hex(16))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USE_SMTP = True
    CSRF_ENABLE = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_HOST = "localhost"
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PW = os.getenv("DB_PW")
    DB_PORT = os.getenv("DB_PORT")
    DB_URI = os.getenv("DB_URI")
    POSTGRES = {
        "user": DB_USER,
        "pw": DB_PW,
        "host": DB_HOST,
        "port": DB_PORT,
        "db": DB_NAME,
    }
    SQLALCHEMY_DATABASE_URI = DB_URI%POSTGRES
    #@property
    #def SQLALCHEMY_DATABASE_URI(self):
    #    return self.DB_URI % self.POSTGRES


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = False


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "bad_key"
