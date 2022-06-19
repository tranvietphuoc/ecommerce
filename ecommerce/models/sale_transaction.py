from ecommerce.extensions import db


class SaleTransaction(db.Model):
    """Sale transaction table"""

    __tablename__ = "saletransaction"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.DECIMAL, nullable=False)
    cc_number = db.Column(db.String(50), nullable=False)
    cc_type = db.Column(db.String(50), nullable=False)
    response = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<OrderTransaction('{self.id}', '{self.order_id}',\
        '{self.amount}', '{self.cc_number}', '{self.cc_type}',\
        '{self.response}', '{self.transaction_date}')>"

    def __str__(self):
        return f"Transaction: {self.id} on {self.transaction_date}"
