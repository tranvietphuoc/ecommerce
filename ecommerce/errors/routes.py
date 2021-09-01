from flask import Blueprint, render_template
from ..models import db, Category
from werkzeug.exceptions import HTTPException
import json


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(HTTPException)
def handle_exception(e):
    """Generic exception handlers. Return JSON instead HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {"code": e.code, "name": e.name, "description": e.description}
    )
    response.content_type = "application/json"
    return response


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
