from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length


class CheckoutForm(FlaskForm):
    full_name = StringField(
        "Full name:",
        validators=[DataRequired()],
        render_kw={"placeholder": "Full name"},
    )
    email = StringField(
        "Email:",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    address = StringField(
        "Address:", validators=[DataRequired()], render_kw={"placeholder": "Address"}
    )
    city = StringField(
        "City:", validators=[DataRequired()], render_kw={"placeholder": "City"}
    )
    state = StringField("State:", render_kw={"placeholder": "State"})
    zipcode = StringField(
        "Zip code:",
        validators=[Length(min=2, max=6)],
        render_kw={"placeholder": "Zip code"},
    )
    cctype = RadioField("Card type:")
    card_name = StringField(
        "Card name:",
        validators=[DataRequired(), Length(min=12, max=12)],
        render_kw={"placeholder": "Card name"},
    )
    ccnumber = StringField("Credit card number:", validators=[DataRequired()])
    expire = DateField("Expire at:", validators=[DataRequired()], format="%Y-%m")
    cvv = StringField("CVV", validators=[DataRequired(), Length(min=3, max=3)])
    submit = SubmitField("Make payment")
