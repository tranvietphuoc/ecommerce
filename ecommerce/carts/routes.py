from ..models import Cart, db, Product
from flask import Blueprint, redirect, render_template, url_for, request


carts = Blueprint("carts", __name__)


@carts.route("/carts/<string:checkout>", methods=("GET", "POST"))
def checkout():
    """Checkout cart."""
    pass


@carts.route("/carts/<int:product_id>/add", methods=("GET", "POST"))
def add_to_cart(product_id):
    """Add product with product_id to cart."""
    pass


@carts.route("/carts/<int:product_id>/delete", methods=("GET", "POST"))
def delete_from_cart(product_id):
    """Delete product with product_id from cart."""
    pass
