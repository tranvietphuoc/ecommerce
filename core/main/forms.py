from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import request


class SearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])

    submit = SubmitField("Search")

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "csrf_enabled" not in kwargs:
            kwargs["csrf_enabled"] = False
        super(SearchForm, self).__init__(*args, **kwargs)
