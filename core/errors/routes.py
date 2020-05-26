from flask import Blueprint, render_template
from core.models import db, Category


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    categories = db.session.query(Category).all()
    return render_template("errors/404.html", categories=categories), 404


@errors.app_errorhandler(403)
def error_403(error):
    categories = db.session.query(Category).all()
    return render_template("errors/403.html", categories=categories), 403


@errors.app_errorhandler(500)
def error_500(error):
    categories = db.session.query(Category).all()
    return render_template("errors/500.html", categories=categories), 500
