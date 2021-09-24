from ecommerce.extensions import db


class Cart(db.Model):
    """Cart table"""

    __tablename__ = "cart"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        primary_key=True,
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=True
    )
    quantity = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Cart('{self.user_id}', '{self.product_id}',\
            '{self.quantity}')>"
