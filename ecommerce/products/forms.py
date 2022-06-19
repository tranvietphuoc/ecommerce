from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectMultipleField,
    IntegerField,
    FloatField,
)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    categories = SelectMultipleField("Category:", choices=[])
    sku = IntegerField(
        "Product SKU:",
        validators=[DataRequired()],
        render_kw={"placeholder": "SKU"},
    )
    product_name = StringField(
        "Product name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product name"},
    )
    product_price = FloatField(
        "Product price:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product price"},
    )
    product_quantity = IntegerField(
        "Product quantity:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product quantity"},
    )
    product_description = StringField(
        "Product description:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product description"},
    )
    product_image = FileField(
        "Product image:", validators=[FileAllowed(["jpg", "jpeg", "png"])]
    )
    submit = SubmitField("Save")


class UpdateProductForm(FlaskForm):
    categories = SelectMultipleField("Category", choices=[])
    sku = IntegerField(
        "Product SKU:",
        validators=[DataRequired()],
        render_kw={"placeholder": "SKU"},
    )
    product_name = StringField(
        "Product name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product name"},
    )
    product_price = FloatField(
        "Product price:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product price"},
    )
    product_discounted_price = FloatField(
        "Discounted price:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Discounted price"},
    )
    product_quantity = IntegerField(
        "Product quantity:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product quantity"},
    )
    product_description = StringField(
        "Product description:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Product description"},
    )
    product_image = FileField(
        "Product image:", validators=[FileAllowed(["jpg", "jpeg", "png"])]
    )
    submit = SubmitField("Update")
