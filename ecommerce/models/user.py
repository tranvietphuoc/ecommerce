from flask import url_for, flash, redirect
from ecommerce.extensions import db
from flask_login import UserMixin
from ecommerce.models.role import RoleMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, jsonify
from werkzeug.security import check_password_hash
from ecommerce.extensions import login_manager
import typing as t


# login manager
login_manager.login_view = "users.login"  # use blueprint
login_manager.login_message_category = "info"


# this decorater is used to handle session
@login_manager.user_loader
def load_user(user_id: t.Optional[int]):
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
    flash("You must be logged in.", "info")
    return redirect(url_for("users.login"))


# define an linking table in relationship with Role and User model
# many-to-many relationship
users_roles = db.Table(
    "users_roles",
    db.Column(
        "user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True
    ),
    db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True
    ),
)


class User(db.Model, UserMixin, RoleMixin):
    """User table"""

    # must have __tablename__ with lower case
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    full_name = db.Column(db.String(60))
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), default="")
    city = db.Column(db.String(20), default="")
    state = db.Column(db.String(20), default="")
    country = db.Column(db.String(20), default="")
    zipcode = db.Column(db.String(20), default="")
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    profile_picture = db.Column(
        db.String(200), nullable=False, default="default.jpg"
    )
    is_superuser = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        "Role",
        secondary="users_roles",
        primaryjoin=(users_roles.c.user_id == id),
        secondaryjoin=None,
        backref=db.backref("users", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<User('{self.id}', '{self.user_name}', '{self.email}', '{self.phone}')>"

    def __str__(self):
        return f"User: {self.user_name}"

    # required for adminitrative interface
    def __unicode__(self):
        return self.user_name

    @property
    def serialize(self):
        """Serialize data from User table."""

        return jsonify({"name": self.first_name + self.last_name})

    # define a method to get reset token, life time is 30 minutes
    def get_reset_token(self, expire=1800):
        """Send a verify token to user's email."""

        s = Serializer(current_app.secret_key)  # exprire = 1800 s
        return s.dumps({"user_id": self.get_id()}).decode("utf-8")

    @staticmethod
    def verify_password(form):
        """Utility for check login password"""

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            return check_password_hash(user.password, form.password.data)

    @staticmethod
    def verify_reset_token(token: t.Optional[str]):
        """Utility for verify reset password token"""

        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(int(user_id))
