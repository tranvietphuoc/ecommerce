from ecommerce.models import Cart, Product, User, db, OrderedProduct
from flask_login import current_user
from flask import session, flash, redirect, url_for


def get_cart_info():
    return


def remove_ordered_product_from_cart(user_id):
    db.session.query(Cart).filter(Cart.user_id == user_id).delete()
    db.session.commit()


def add_ordered_products(user_id, order_id):
    """Add products have been ordered to OrderedProduct table"""
    cart = Cart.query.with_entities(Cart.product_id, Cart.quantity).filter(
        Cart.user_id == user_id
    )
    for item in cart:
        orderd_product = OrderProduct(
            order_id=order_id, product_id=item.product_id, quantity=item.quantity
        )
        db.session.add(orderd_product)
        db.session.flush()
        db.session.commit()


def remove_product_from_cart(product_id):
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
