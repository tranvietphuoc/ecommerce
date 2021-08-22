from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SelectMultipleField, SubmitField, StringField


class AddCategoryForm(FlaskForm):
    category_name = StringField(
        "Category name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Category name"},
    )
    submit = SubmitField("Add")


class UpdateCategoryForm(FlaskForm):
    category_name = StringField(
        "Category name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Category name"},
    )
    products = SelectMultipleField("All products: ", choices=[])
    submit = SubmitField("Update")
