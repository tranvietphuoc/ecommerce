from ecommerce.search import SearchableMixin
from ecommerce.extensions import db
from flask import jsonify
from datetime import datetime


# An linking table to perform many-to-many relationship
# between Product and Category
products_categories = db.Table(
    "products_categories",
    db.Column(
        "product_id",
        db.Integer,
        db.ForeignKey("product.id"),
        primary_key=True,
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("category.id"),
        primary_key=True,
    ),
)


# produc table
class Product(SearchableMixin, db.Model):
    """Product table. Has many-to-many with Category table."""

    __tablename__ = "product"
    __table_args__ = {"extend_existing": True}
    __searchable__ = ["product_name"]

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.DECIMAL, nullable=True)
    discounted_price = db.Column(db.DECIMAL, default=0)
    product_rating = db.Column(db.DECIMAL)
    product_review = db.Column(db.String(100), nullable=True)
    product_image = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # for many-to-one relationship
    # ForeignKey with Category table
    # category_id = db.Column(
    #    db.Integer, db.ForeignKey("category.category_id"), nullable=False
    # )

    # many-to-many relationship with Category table
    categories = db.relationship(
        "Category",
        secondary=products_categories,
        primaryjoin=(products_categories.c.product_id == id),
        secondaryjoin=None,
        backref=db.backref("products", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<Product('{self.id}', '{self.product_name}', '{self.sku}',\
        '{self.product_image}', '{self.quantity}', '{self.product_price}',\
        '{self.discounted_price}', '{[c for c in self.categories]}',\
        '{self.date_added}')>"

    def __str__(self):
        return f"Product: {self.product_name} - quantity: {self.quantity}"

    @property
    def serialize(self):
        return jsonify(
            {
                "Product name": self.product_name,
                "Product description": self.product_description,
                "Product quantity": self.product_quantity,
                "Product price": self.product_price,
            }
        )
