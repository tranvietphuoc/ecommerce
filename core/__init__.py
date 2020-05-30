from flask import Flask, request
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from core.config import Config
from core.admin.views import AdminView, ModelView
import click
from werkzeug.security import generate_password_hash
from flask_script import prompt_pass, prompt_bool, prompt
from flask_babel import Babel
from elasticsearch import Elasticsearch


# initialize all extensions
mail = Mail()
babel = Babel()

login_manager = LoginManager()
login_manager.login_view = "users.login"  # use blueprint
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    """Create Flask app with some extensions"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # elasticsearch
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    # init all extensions with flask app
    # first import from models
    from core.models import db, User, Product, Category, Order, Role

    # init db
    db.init_app(app)

    # setup security
    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # security = Security(app, user_datastore)

    # init other extensions
    login_manager.init_app(app)
    mail.init_app(app)

    # babel
    babel.init_app(app)
    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(app.config['LANGUAGE'])

    # Admin panel follow db
    admin = Admin(app, name="E-commerce admin")
    # add views for admin
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Product, db.session))
    admin.add_view(AdminView(Category, db.session))
    admin.add_view(AdminView(Order, db.session))
    admin.add_view(AdminView(Role, db.session))

    # initialize migrating database
    migrate = Migrate()
    migrate.init_app(app, db)

    # import all routes of blueprints here
    from core.users.routes import users
    from core.main.routes import main
    from core.errors.routes import errors
    from core.products.routes import products
    from core.cart.routes import cart

    # then register these blueprints here
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(products)
    app.register_blueprint(cart)

    # define some utilities if use flask command
    @app.shell_context_processor
    def shell_context():
        return dict(app=app, db=db, User=User, Category=Category)

    # before first request, create roles
    @app.before_first_request
    def create_role():
        query = db.session.query(Role).all()
        if not query:
            db.session.add(Role(role_name="superuser"))
            db.session.add(Role(role_name="user"))
            db.session.commit()
            print("Roles have been created.")

    @app.cli.command("create")
    @click.argument("superuser")
    def create_superuser(superuser):
        """Create superuser with CLI interface."""
        name = prompt("Enter superuser name. Default", default="admin")
        email = prompt("Enter superuser email", default="admin@email.com")
        password = prompt_pass("Enter pasword")
        if not User.query.filter_by(user_name=name).first():
            user = User(
                user_name=name,
                email=email,
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
        if prompt_bool("Are you sure to drop database"):
            db.drop_all()

    return app
