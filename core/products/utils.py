from core.models import Product, Category, db
import os
from flask import current_app
import PIL
import hashlib


def get_product_detail(product_id):
    return Product.query.filter(Product.product_id == product_id).first_or_404()


def save_product_image(form_image, product_name):
    _, file_ext = os.path.splitext(form_image.filename)
    image_name = (
        hashlib.sha256(product_name.encode("utf-8")).hexdigest() + file_ext
    )
    image_path = os.path.join(
        current_app.root_path, "static/assets/products", image_name
    )
    img = PIL.Image.open(form_image)
    img.save(image_path)
    return image_name
