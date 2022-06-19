from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    flash,
    url_for,
    make_response,
)
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash
from .forms import (
    RegistrationForm,
    LoginForm,
    UpdateForm,
    SendResetTokenForm,
    ResetPasswordForm,
)
from ..models import User, db, Role, Category
from ..utils import save_picture, send_reset_token
from flask_babel import _
import typing as t
from ..logs import logger


users = Blueprint("users", __name__)


@users.route("/register", methods=("GET", "POST"))
def register():
    """Register."""

    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    categories = db.session.query(Category).all()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)

        user = User(
            user_name=form.user_name.data,
            full_name=form.full_name.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
        )
        db.session.add(user)
        db.session.flush()
        # add role for user
        user_role = db.session.query(Role).filter_by(role_name="user").first()
        user_role.users.append(user)
        db.session.commit()
        flash(
            _(f"Your account have been created. You are now able to log in."),
            "success",
        )
        return redirect(url_for("users.login"))
        all_users_phone_numbers = [u.phone for u in db.session.query(User).all()]
        all_users_emails = [u.email for u in db.session.query(User).all()]

        if form.phone.data in all_users_phone_numbers:
            flash(_("Phone number already exists in another account"), "danger")
        elif form.email.data in all_users_emails:
            flash(_("Email already exists in another account"), "danger")
        else:
            user = User(
                user_name=form.user_name.data,
                full_name=form.full_name.data,
                email=form.email.data,
                password=hashed_password,
                phone=form.phone.data,
            )
            db.session.add(user)
            db.session.flush()

            # add role for user
            user_role = db.session.query(Role).filter_by(role_name="user").first()
            user_role.users.append(user)  # add roles to user
            db.session.commit()
            logger.info("Your account have been created.")
            flash(
                _(f"Your account have been created. You are now able to log in."),
                "success",
            )

            return redirect(url_for("users.login"))
    return render_template(
        "user/register.html",
        title=_("Register"),
        form=form,
        categories=categories,
    )


@users.route("/login", methods=("GET", "POST"))
def login():
    """Log in"""
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    categories = db.session.query(Category).all()
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and User.verify_password(form):
            # login to user, add remember_me
            login_user(user, remember=form.remember_me.data)
            logger.info("Login success.")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home.index"))
        else:
            flash(
                _("Login unsuccessful. Please check your email and password"),
                "danger",
            )
    resp = make_response(
        render_template(
            "user/login.html",
            title=_("Sign in"),
            form=form,
            categories=categories,
        )
    )
    return resp


@users.route("/logout", methods=("GET", "POST"))
def logout():
    """Log out"""
    logout_user()
    logger.info("Logged out.")
    return redirect(url_for("users.login"))


@users.route("/about", methods=("GET", "POST"))
@login_required
def about():
    """Update user information"""
    categories = db.session.query(Category).all()
    form = UpdateForm(current_user.user_name)  # fix duplicate username bug
    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture = save_picture(
                form.profile_picture.data, current_user.user_name
            )
            current_user.profile_picture = profile_picture
        if form.user_name.data:
            current_user.user_name = form.user_name.data
        if form.email.data:
            current_user.email = form.email.data
        if form.new_password.data:
            current_user.password = generate_password_hash(
                form.new_password.data
            ).decode("utf-8")
        if form.address.data:
            current_user.address = form.address.data
        if form.city.data:
            current_user.city = form.city.data
        if form.state.data:
            current_user.state = form.state.data
        if form.zipcode.data:
            current_user.zipcode = form.zipcode.data
        if form.phone.data:
            current_user.phone = form.phone.data
        db.session.commit()
        logger.info("Your account have been updated.")
        flash(_("Your account have been updated."), "success")
        return redirect(url_for("users.about"))
    elif request.method == "GET":
        form.email.data = current_user.email
    picture = url_for("static", filename="assets/users/" + current_user.profile_picture)
    return render_template(
        "user/about.html",
        title=_("About"),
        picture=picture,
        form=form,
        categories=categories,
    )


@users.route("/reset", methods=("GET", "POST"))
def send_reset():
    """Send reset token to user's email"""
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    categories = db.session.query(Category).all()
    form = SendResetTokenForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_token(user)
        logger.info("Success send reset token to email.")
        flash(_("An email sent with instructions to reset your password."), "info")
        redirect(url_for("users.login"))
    return render_template(
        "user/reset_request.html",
        title=_("Send reset token"),
        form=form,
        categories=categories,
    )


@users.route("/reset/<string:token>", methods=("GET", "POST"))
def reset_password(token: t.Optional[str]):
    """Confirm reset token and save new password"""
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    user = User.verify_reset_token(token)  # verify reset token
    if not user:
        flash(_("This token is invalid."), "warning")
        return redirect(url_for("users.send_reset"))

    categories = db.session.query(Category).all()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        logger.info("Reset password success.")
        flash(
            _("Your password have been updated. You are now able to login."),
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "user/reset_token.html",
        title=_("Reset password"),
        form=form,
        categories=categories,
    )
