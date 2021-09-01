from ..extensions import db
from datetime import datetime


class Order(db.Model):
    """Order table"""

    __tablename__ = "order"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    total_price = db.Column(db.DECIMAL, nullable=False)
    ordered_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order('{self.id}', '{self.order_date}',\
        '{self.total_price}', '{self.user_id}'>"

    def __str__(self):
        return f"Order: {self.order_id} on {self.order_date}"
