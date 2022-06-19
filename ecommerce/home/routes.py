from flask import (
    Blueprint,
    render_template,
    request,
    g,
    redirect,
    url_for,
    current_app,
)
from ..models import db, Category, Product
from .forms import SearchForm
from flask_login import current_user
from datetime import datetime


home = Blueprint("home", __name__)


@home.route("/", methods=("GET", "POST"))
@home.route("/home", methods=("GET", "POST"))
def index():
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


@home.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.seach_form = SearchForm()

    # g.locale = str(get_locale())


@home.route("/search")
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for(""))
    page = request.args.get("page", 1, type=int)
    posts, total = Product.search(
        g.search_form.q.data, page, current_app.config["PRODUCT_PER_PAGE"]
    )
    next_url = (
        url_for("main.search", q=g.search_form.q.data, page=page + 1)
        if total > page * current_app.config["POST_PER_PAGE"]
        else None
    )
    previous_url = (
        url_for("main.search", q=q.search_form.data, page=page - 1)
        if page > 1
        else None
    )
    return render_template(
        "search.html",
        title=_("Search"),
        posts=posts,
        next_url=next_url,
        previous_url=previous_url,
    )
