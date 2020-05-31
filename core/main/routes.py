from flask import Blueprint, render_template, request, g, redirect, url_for
from core.models import db, Category, Product
from core.main.forms import SearchForm
from flask_login import current_user
from datetime import datetime


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
    return render_template(
        "home.html", title="Home", categories=categories, products=products
    )


@main.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.seach_form = SearchForm()

    # g.locale = str(get_locale())


@main.route("/search")
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for(""))
    page = request.args.get("page", 1, type=int)
