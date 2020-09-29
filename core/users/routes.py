from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required, login_user, current_user, logout_user
from core.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateForm,
    SendResetTokenForm,
    ResetPasswordForm,
)
from werkzeug.security import generate_password_hash
from core.models import User, db, Role, Category
from core.users.utils import save_picture, send_reset_token


users = Blueprint("users", __name__)


@users.route("/register", methods=("GET", "POST"))
def register():
    """Register"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    categories = db.session.query(Category).all()
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            user_name=form.user_name.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            country=form.country.data,
            email=form.email.data,
            password=hashed_password,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zipcode=form.zipcode.data,
            phone=form.phone.data,
        )
        db.session.add(user)
        db.session.flush()
        # add role for user
        user_role = db.session.query(Role).filter_by(role_name="user").first()
        user_role.users.append(user)
        db.session.commit()
        flash(
            f"Your account have been created. You are now able to log in.", "success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "user/register.html", title="Register", form=form, categories=categories
    )


@users.route("/login", methods=("GET", "POST"))
def login():
    """Log in"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    categories = db.session.query(Category).all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and User.verify_password(form):
            # login to user, add remember_me
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash(f"Login unsuccessful. Please check email and password", "danger")
    return render_template(
        "user/login.html", title="Sign in", form=form, categories=categories
    )


@users.route("/logout", methods=("GET", "POST"))
def logout():
    """Log out"""
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/about", methods=("GET", "POST"))
@login_required
def about():
    """Update user information"""
    categories = db.session.query(Category).all()
    form = UpdateForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture = save_picture(
                form.profile_picture.data, current_user.user_name
            )
            current_user.profile_picture = profile_picture
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
        flash(f"Your account have been updated.", "success")
        return redirect(url_for("users.about"))
    elif request.method == "GET":
        form.email.data = current_user.email
    picture = url_for("static", filename="assets/users/" + current_user.profile_picture)
    return render_template(
        "user/about.html",
        title="About",
        picture=picture,
        form=form,
        categories=categories,
    )


@users.route("/reset", methods=("GET", "POST"))
def send_reset():
    """Send reset token to user's email"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    categories = db.session.query(Category).all()
    form = SendResetTokenForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_token(user)
        flash(f"An email sent with instructions to reset your password.", "info")
        redirect(url_for("users.login"))
    return render_template(
        "user/reset_request.html",
        title="Send reset token",
        form=form,
        categories=categories,
    )


@users.route("/reset/<string:token>", methods=("GET", "POST"))
def reset_password(token):
    """Confirm reset token and save new password"""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)  # verify reset token
    if not user:
        flash(f"This token is invalid.", "warning")
        return redirect(url_for("users.send_reset"))

    categories = db.session.query(Category).all()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash(
            f"Your password have been updated. You are now able to login.", "success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "user/reset_token.html",
        title="Reset password",
        form=form,
        categories=categories,
    )
