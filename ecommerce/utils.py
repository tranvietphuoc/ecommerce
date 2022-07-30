from flask import url_for, current_app, session, flash, redirect
from ecommerce import mail
from flask_mail import Message
from PIL import Image
from .models import db, User, Cart, Product, Category
import hashlib
import typing as t
from pathlib import Path


# Save profile picture
def save_picture(form_picture: t.Any, user_name: t.Optional[str]) -> str:
    file_ext = Path(form_picture.filename).suffix
    picture_name = (
        hashlib.sha256(user_name.encode("utf-8")).hexdigest()[0:16] + file_ext
    )
    picture_path = (
        Path(current_app.root_path)
        .joinpath("static/assets/users")
        .joinpath(picture_name)
        .resolve()
    )

    output_size = (100, 100)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_name


# send reset token to mail of user
def send_reset_token(user: t.Optional[int]):
    token = user.get_reset_token()
    msg = Message(
        "Password reset request",
        sender="noreply@gmail.com",
        recipients=[user.email],
    )
    msg.body = f"""
    To reset your password, visit the following link:
    {url_for('users.reset_password', token=token, _external=True)}
    If you did not make this request, please ignore this email changes be made
    """
    mail.send(msg)


# cart
def get_cart_info():
    # not complete yet
    return


def remove_order_from_cart(user_id: t.Optional[int]):
    # not complete yet
    db.session.query(Cart).filter(Cart.user_id == user_id).delete()
    db.session.commit()


def add_ordered_products(user_id: t.Optional[int], order_id: t.Optional[int]):
    # not complete yet
    """Add products have been ordered to OrderedProduct table"""
    cart = Cart.query.with_entities(Cart.product_id, Cart.quantity).filter(
        Cart.user_id == user_id
    )
    for item in cart:
        orderd_product = OrderProduct(
            order_id=order_id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.session.add(orderd_product)
        db.session.flush()
        db.session.commit()


# product
def remove_product_from_cart(product_id: t.Optional[int]):
    # not complete yet
    userID = (
        User.query.with_entities(User.user_id)
        .filter(User.email == session["email"])
        .first()
    )
    user_id = userID[0]
    kwargs = {"user_id": user_id, "product_id": product_id}
    cart = Cart.query.filter_by(**kwargs).first()
    if product_id is not None:
        db.session.delete(cart)
        db.session.commit()
        flash("Product has been remove from cart.", "success")
    else:
        flash("Failed to remove product cart, please try again.", "danger")
    return redirect(url_for("cart/cart.html"))


def get_product_detail(product_id: t.Optional[int]):

    return Product.query.filter(Product.product_id == product_id).first_or_404()


def save_product_image(form_image: t.Any, product_name: t.Optional[str]) -> str:

    # _, file_ext = os.path.splitext(form_image.filename)
    file_ext = Path(form_image.filename).suffix

    image_name = (
        hashlib.sha256(product_name.encode("utf-8")).hexdigest()[0:16]
        + file_ext
    )
    image_path = (
        Path(current_app.root_path)
        .joinpath("static/assets/products")
        .joinpath(image_name)
        .resolve()
    )
    img = Image.open(form_image)
    img.save(image_path)
    return image_name
