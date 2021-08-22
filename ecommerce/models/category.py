from ecommerce.extensions import db
from ecommerce.search import SearchableMixin
from datetime import datetime


class Category(SearchableMixin, db.Model):
    """Category table. Has many-to-many relationship with Product table."""

    __tablename__ = "category"
    __table_args__ = {"extend_existing": True}
    __searchable__ = ["category_name"]

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # one to many relationship with Product table
    # products = db.relationship(
    #     "Product", backref=db.backref("category", lazy="select")
    # )

    def __repr__(self):
        return f"<Category('{self.id}', '{self.category_name}')>"

    def __str__(self):
        return f"Category: {self.category_name}"
