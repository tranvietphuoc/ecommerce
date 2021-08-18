from flask import Blueprint, json
from ecommerce.models import Product
from ecommerce.api.schemas import ProductSchema
from ecommerce.api.encoders import DecimalEncoder


pro = Blueprint('pro', __name__)


@pro.route("/api/v1/product/list", methods=['GET'])
def get_products():
    products = Product.query.all()
    schema = ProductSchema(many=True)

    return json.dumps(schema.dump(products), cls=DecimalEncoder)

