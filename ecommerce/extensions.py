from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate
from flask_login import LoginManager
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


# mail
mail = Mail()

# babel
babel = Babel()

# sqlalchemy
db = SQLAlchemy()

# migrate
migrate = Migrate()

# login manager
login_manager = LoginManager()

spec = APISpec(
    title="Ecommerce",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="A minimal Ecommerce API"),
    contact=dict(email="phuoc.finn@gmail.com"),
    plugins=[
        MarshmallowPlugin(),
        FlaskPlugin(),
    ],
)
