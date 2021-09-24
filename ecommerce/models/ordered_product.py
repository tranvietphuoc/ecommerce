from ecommerce.extensions import db


class OrderedProduct(db.Model):
    """Ordered product table"""

    __tablename__ = "orderedproduct"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<OrderProduct('{self.id}', '{self.order_id}',\
        '{self.product_id}', '{self.quantity}')>"
