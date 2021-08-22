"""
This package contain all models of the app and more add-on includes
"""

from flask import url_for, flash, redirect
from ecommerce.extensions import login_manager
from ecommerce.search import SearchableMixin
from ecommerce.models.user import *
from ecommerce.models.product import *
from ecommerce.models.role import *
from ecommerce.models.cart import *
from ecommerce.models.category import *
from ecommerce.models.order import *
from ecommerce.models.ordered_product import *
from ecommerce.models.sale_transaction import *


# login manager
login_manager.login_view = "users.login"  # use blueprint
login_manager.login_message_category = "info"

# elasticsearch config
db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)


# this decorater is used to handle session
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login keeps track of the logged in user by storing
    its unique identifier in Flask's user session,
    Flask-Login retrieves the ID of the user from the session,
    and then loads that user into memory.
    """

    return User.query.get(user_id)


@login_manager.request_loader
def load_request(request):
    user_name = request.form.get("user_name")
    user = User.query.filter_by(user_name=user_name).first()
    return user if user else None


@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in.")
    return redirect(url_for("users.login"))

