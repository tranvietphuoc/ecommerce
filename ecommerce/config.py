"""
Configuration of flask environment variables.
"""

import os
from dotenv import load_dotenv
import secrets
import tempfile

# from apispec import APISpec
# from apispec.ext.marshmallow import MarshmallowPlugin
from pathlib import Path


project = Path(__file__).parent.parent  # __file__ in .../Ecommerce/ecommerce/
env = project.joinpath(".env").resolve()  # get abspath for .env
load_dotenv(env, override=True)
API_TITLE = os.getenv("API_TITLE")
VERSION = os.getenv("VERSION")
OPENAPI_VERSION = os.getenv("OPENAPI_VERSION")


class Config:
    DEBUG = True
    TESTING = False
    CORS_HEADER = os.getenv("CORS_HEADER")
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
    SQLALCHEMY_DATABASE_URI = DB_URI % POSTGRES
    LANGUAGES = ["en", "vi"]
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
    FLASK_ADMIN_SWATCH = os.getenv("FLASK_ADMIN_SWATCH")
    # APISPEC_SPEC = APISpec(
    #     title=API_TITLE,
    #     version=VERSION,
    #     plugins=[MarshmallowPlugin()],
    #     openapi_version=OPENAPI_VERSION
    # )

    # @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #    return self.DB_URI % self.POSTGRES


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = secrets.token_hex(8)
    SQLALCHEMY_TRACK_MODIFICATION = False


class TestingConfig(Config):
    # db_fd, db_path = tempfile.mkdtemp()
    TESTING = True
    SECRET_KEY = "im_bad_key"
    # DB_URI = db_path


class StagingConfig(Config):
    DEBUG = False
    SECRET_KEY = secrets.token_hex(8)
