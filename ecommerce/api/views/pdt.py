from ecommerce.extensions import spec
from flask import Blueprint, json
from ecommerce.models import Product, db, Category
from ..schemas import ProductSchema
from ..encoders import DecimalEncoder
from sqlalchemy import select
from flask_cors import cross_origin
from flask.views import MethodView


pdt = Blueprint("pdt", __name__, url_prefix="/api/v1/product")


class ProductView(MethodView):
    @cross_origin(origin="*")
    def get(self):
        """
        Product view
        ---
        get:
            description: Get all products from database
            responses:
                200:
                    content:
                        application/json:
                        schema: ProductSchema
        """
        products = db.session.query(Product).all()
        schema = ProductSchema(many=True)
        return json.dumps(schema.dump(products), cls=DecimalEncoder)


products_view = ProductView.as_view("product_view")
spec.components.schema("Ecommerce", schema=ProductSchema)
pdt.add_url_rule("/all", view_func=products_view)
