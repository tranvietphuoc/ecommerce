from flask import Flask, request, current_app
from flask_admin import Admin
from flask_script import prompt_pass, prompt_bool, prompt
import click
from werkzeug.security import generate_password_hash
from elasticsearch import Elasticsearch
from ecommerce.config import Config
from ecommerce.auth.views import AdminView, ModelView
from ecommerce.extensions import mail, babel, migrate, login_manager


def create_app(config_class=Config):
    """Create Flask app with some extensions"""

    app = Flask(__name__)
    app.config.from_object(config_class)

    # elasticsearch
    app.elasticsearch = (
        Elasticsearch([app.config["ELASTICSEARCH_URL"]])
        if app.config["ELASTICSEARCH_URL"]
        else None
    )

    # init all extensions with flask app
    # first import from models
    from ecommerce.models import (
            db,
            User,
            Role,
            Category,
            Product,
            Cart,
            Order,
            OrderedProduct,
            SaleTransaction
    )

    # init db
    db.init_app(app)

    # init other extensions
    login_manager.init_app(app)
    mail.init_app(app)

    # babel
    babel.init_app(app)

    # @babel.localeselector
    # def get_locale():
    #     return request.accept_languages.best_match(current_app.config["LANGUAGES"])

    # Admin panel follow db
    admin = Admin(app, name="E-commerce")

    # add views for admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Cart, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(OrderedProduct, db.session))
    admin.add_view(ModelView(SaleTransaction, db.session))

    # initialize migrating database
    migrate.init_app(app, db)

    # import all routes of blueprints here
    from ecommerce.users.routes import users
    from ecommerce.errors.routes import errors
    from ecommerce.products.routes import products
    from ecommerce.carts.routes import carts
    from ecommerce.main.routes import main


    # then register these blueprints here
    app.register_blueprint(users)
    app.register_blueprint(errors)
    app.register_blueprint(products)
    app.register_blueprint(carts)
    app.register_blueprint(main)


    # apis
    from ecommerce.api.views.products import pro

    app.register_blueprint(pro)

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
            print("Roles have been created.")

    @app.cli.command("create")
    @click.argument("superuser")
    def create_superuser(superuser):
        """Create superuser with CLI interface."""

        name = prompt("Enter superuser name.", default="superuser")
        email = prompt("Enter superuser email.", default="superuser@email.com")
        phone_number = prompt("Enter superuser phone number.", default="0111111111")
        password = prompt_pass("Enter pasword")
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
            print(f"User {name} has been created.")
        else:
            print(f"User {name} already existed in database.")

    @app.cli.command("dropdb")
    def drop_db():
        """Drop database."""

        if prompt_bool("Are you sure to drop database? [y/N]:"):
            db.drop_all()

    # asgi_app = WsgiToAsgi(app)
    # return asgi_app
    return app
