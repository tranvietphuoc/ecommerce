from flask import Blueprint, render_template, request
from core.models import db, Category, Product


main = Blueprint("main", __name__)


@main.route("/", methods=("GET", "POST"))
@main.route("/home", methods=("GET", "POST"))
def home():
    categories = db.session.query(Category).all()
    page = request.args.get("page", 1, type=int)
    products = (
        db.session.query(Product)
        .order_by(Product.product_rating.desc())
        .paginate(page=page, per_page=20)
    )
    return render_template("home.html", title="Home", categories=categories, products=products)


@main.route("/search", methods=("GET", "POST"))
def search():
    pass
