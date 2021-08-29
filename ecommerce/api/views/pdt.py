from flask import Blueprint, json
from ecommerce.models import Product, db, Category
from ..schemas import ProductSchema
from ..encoders import DecimalEncoder
from sqlalchemy import select
from flask_cors import cross_origin


pdt = Blueprint('pdt', __name__)


@pdt.get("/api/v1/product/list")
@cross_origin(origin='*')
def get_products():
    # stmt = select(Product).join(Product.categories)
    # products = db.session.query(Product, Category).filter(Product.categories ==
    #         Category.id).all()
    products = db.session.query(Product).all()
    schema = ProductSchema(many=True)

    return json.dumps(schema.dump(products), cls=DecimalEncoder)
    # print(stmt)
