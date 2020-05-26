from flask import Blueprint, render_template, request
from core.models import db, Category


main = Blueprint("main", __name__)


@main.route("/", methods=("GET", "POST"))
@main.route("/home", methods=("GET", "POST"))
def home():
    categories = db.session.query(Category).all()
    page = request.args.get("page", 1, type=int)
    return render_template("home.html", title="Home", categories=categories)


@main.route("/search", methods=("GET", "POST"))
def search():
    pass
