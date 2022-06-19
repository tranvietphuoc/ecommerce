from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    EqualTo,
    DataRequired,
    Email,
    Length,
    ValidationError,
)
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User


class RegistrationForm(FlaskForm):
    user_name = StringField(
        "User name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "User name"},
    )
    full_name = StringField(
        "Full name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Full name"},
    )
    email = StringField(
        "Email:",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Confirm password:",
        render_kw={"placeholder": "Confirm password"},
        validators=[DataRequired(), EqualTo("password")],
    )
    phone = StringField(
        "Phone:",
        validators=[DataRequired(), Length(min=10, max=12)],
        render_kw={"placeholder": "Phone"},
    )
    submit = SubmitField("Sign up")

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError(
                "This user name is taken.\
                Please choose another one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is taken.\
                Please choose another one."
            )


class LoginForm(FlaskForm):
    email = StringField(
        "Email:",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Sign in")
    remember_me = BooleanField("Remember me:")


class UpdateForm(FlaskForm):
    """Need to input password to update, another fields is not needed"""

    full_name = StringField(
        "Full name:", render_kw={"placeholder": "Full name"}
    )
    email = StringField("Email:", render_kw={"placeholder": "Email"})
    profile_picture = FileField(
        "Update profile picture:",
        validators=[FileAllowed(["jpg", "png", "jpeg"])],
    )
    old_password = PasswordField(
        "Old password:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Old password"},
    )
    new_password = PasswordField(
        "New password:", render_kw={"placeholder": "New password"}
    )
    confirm_password = PasswordField(
        "Confirm password:",
        validators=[EqualTo("new_password")],
        render_kw={"placeholder": "Confirm password"},
    )
    country = StringField("Country:", render_kw={"placeholder": "Country"})

    address = StringField("Address:", render_kw={"placeholder": "Address"})
    city = StringField("City:", render_kw={"placeholder": "City"})
    state = StringField("State:", render_kw={"placeholder": "State"})
    zipcode = StringField("Zip code:", render_kw={"placeholder": "Zip code"})
    phone = StringField(
        "Phone:",
        validators=[Length(min=12, max=12)],
        render_kw={"placeholder": "Phone"},
    )
    submit = SubmitField("Update")

    def validate_password(self, old_password):
        o_pw_h = generate_password_hash(old_password.data).decode("utf-8")
        if not check_password_hash(o_pw_h, current_user.password):
            raise ValidationError(
                "Your old password is incorrect. Please try again."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email is taken. Please choose another one."
            )


class ResetPasswordForm(FlaskForm):
    """Set new password"""

    password = PasswordField(
        "Password:",
        validators=[DataRequired()],
        render_kw={"placeholder": "New password"},
    )
    confirm_password = PasswordField(
        "Confirm password:",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm password"},
    )
    submit = SubmitField("Reset")


class SendResetTokenForm(FlaskForm):
    """Send reset token to user's email to set new password"""

    email = StringField(
        "Email:",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    submit = SubmitField("Send")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email.\
                You must register first."
            )
