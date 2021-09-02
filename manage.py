"""
This module is used if you want to run app like django.
But you have to install flask_script first.
"""

from ecommerce import create_app
from ecommerce import models
from ecommerce.models import db, Role, Category, User
from flask_script import (
    Manager,
    Shell,
    Server,
    prompt_bool,
    prompt_pass,
    prompt,
)
from flask_migrate import MigrateCommand
from werkzeug.security import generate_password_hash


def _make_context():
    return dict(app=create_app(), db=db, models=models, User=User, Category=Category)


class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        with create_app().app_context():
            query = db.session.query(Role).all()
            if not query:
                db.session.add(Role(role_name="superuser"))
                db.session.add(Role(role_name="admin"))
                db.session.add(Role(role_name="user"))
                db.session.commit()
                print("Roles have been created.")
        return Server.__call__(self, app, *args, **kwargs)


manager = Manager(create_app)
manager.add_command("db", MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))
# manager.add_command("runserver", CustomServer())
manager.add_command("runserver", CustomServer())


@manager.command
def dropdb():
    """Drop database."""
    if prompt_bool("Are you sure to drop database"):
        db.drop_all()


@manager.command
@manager.option("-s", "--supseruser", dest="superuser")
def create(superuser):
    """Create superuser with CLI interface."""
    name = prompt("Enter superuser name.", default="superuser")
    email = prompt("Enter superuser email.", default="superuser@email.com")
    phone_number = prompt("Enter superuser phone number.", default="0111111111")
    password = prompt_pass("Enter password")
    if not User.query.filter_by(user_name=name).first():
        user = User(
            user_name=name,
            email=email,
            phone=phone_number,
            password=generate_password_hash(password),
            is_superuser=True,
        )
        db.session.add(user)  # add admin user to database
        superuser_role = db.session.query(Role).filter_by(role_name="superuser").first()
        superuser_role.users.append(user)
        db.session.commit()
        print(f"User {name} has been created.")
    else:
        print(f"User {name} already existed in database.")


if __name__ == "__main__":
    manager.run()
