from core.models import Cart, db, Product
from flask import Blueprint, redirect, render_template, url_for


cart = Blueprint(__name__)


@cart.route("/cart/<string:checkout>", methods=("GET", "POST"))
def checkout():
    pass
