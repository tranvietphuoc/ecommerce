from flask import Blueprint, render_template, request


main = Blueprint("main", __name__)


@main.route("/", methods=("GET", "POST"))
@main.route("/home", methods=("GET", "POST"))
def home():
    page = request.args.get("page", 1, type=int)
    return render_template("home.html", title="Home")


@main.route("/search", methods=("GET", "POST"))
def search():
    pass
