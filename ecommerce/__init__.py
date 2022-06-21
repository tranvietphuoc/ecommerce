from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
import click
from werkzeug.security import generate_password_hash
from elasticsearch import Elasticsearch
from werkzeug.utils import import_string
from .config import Config
from .auth.views import AdminView, ModelView
from .extensions import mail, babel, migrate, login_manager, spec
from .models import *

# import all routes of blueprints here
from .users.routes import users
from .errors.routes import errors
from .products.routes import products
from .categories.routes import categories
from .carts.routes import carts
from .home.routes import home

# apis blueprints
from .api.views.pdt import pdt, ProductView, products_view
import typing as t
from .logs import logger


def create_app(config_class: t.Optional[t.Type[Config]] = Config):
    """Create Flask app with some extensions"""

    app = Flask(__name__)
    app.config.from_object(config_class)

    # cors
    CORS(app)

    # elasticsearch
    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    # init db
    db.init_app(app)

    # init other extensions
    login_manager.init_app(app)

    # mail
    mail.init_app(app)

    # babel
    babel.init_app(app)

    # @babel.localeselector
    # def get_locale():
    #     return request.accept_languages.best_match(current_app.config["LANGUAGES"])

    # Admin panel follow db
    admin = Admin(app, name="E-commerce")

    # apis docs
    # with app.test_request_context():
    #     spec.path(view=products_view)

    # add views for admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Cart, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(OrderedProduct, db.session))
    admin.add_view(ModelView(SaleTransaction, db.session))

    # then register these blueprints here
    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.register_blueprint(products)
    app.register_blueprint(carts)
    app.register_blueprint(home)
    app.register_blueprint(categories)
    app.register_blueprint(pdt)

    # initialize migrating database
    migrate.init_app(app, db)

    # define some utilities if use flask command
    @app.shell_context_processor
    def shell_context():
        return dict(app=app, db=db, User=User, Category=Category)

    # before first request, create roles
    @app.before_first_request
    def create_role():
        """Create two roles when the fisrt run."""
        query = db.session.query(Role).all()
        if not query:
            db.session.add(Role(role_name="superuser"))
            db.session.add(Role(role_name="admin"))
            db.session.add(Role(role_name="user"))
            db.session.commit()

            # print("Roles have been created.")
            app.logger.info("Created roles.")

    @app.cli.command("create")
    @click.argument("superuser")
    def create_superuser(superuser):
        """Create superuser with CLI interface."""

        name = click.prompt("Enter superuser name.", type=str, default="superuser")
        email = click.prompt("Enter superuser email.", default="superuser@email.com")
        phone_number = click.prompt(
            "Enter superuser phone number.", default="0111111111"
        )
        password = click.prompt("Enter pasword.", hide_input=True)
        if not User.query.filter_by(user_name=name).first():
            user = User(
                user_name=name,
                email=email,
                phone=phone_number,
                password=generate_password_hash(password),
                is_superuser=True,
            )
            db.session.add(user)
            db.session.commit()
            superuser_role = (
                db.session.query(Role).filter_by(role_name="superuser").first()
            )
            superuser_role.users.append(user)
            db.session.commit()

            # print(f"User {name} has been created.")
            app.logger.info(f"User {name} has been created.")

        else:

            print(f"User {name} already existed in database.")

            # print(f"User {name} already existed in database.")
            app.logger.info(f"User {name} already existed in database.")

    @app.cli.command("dropdb")
    def drop_db():
        """Drop database."""

        if click.confirm("Are you sure to drop database?"):
            db.drop_all()

            app.logger.info("Successfully drop database")

    return app
