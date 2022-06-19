from flask import (
    Blueprint,
    abort,
    flash,
    render_template,
    redirect,
    url_for,
    request,
    current_app,
)
from ..models import db, Product, Category
from flask_login import current_user
from .forms import (
    AddProductForm,
    UpdateProductForm,
)
from ..utils import save_product_image
from flask_babel import _
import os
import typing as t
from pathlib import Path
from ..logs import logger


products = Blueprint("products", __name__)


@products.route("/admin/products/new", methods=("GET", "POST"))
def add_product():
    """Only superuser can add products."""

    if not current_user.is_authenticated or not current_user.is_active:
        abort(404)  # login to use this function
    else:
        if not current_user.has_role("admin", "superuser"):
            abort(403)  # permission denied
    # get categories from database then add to choices of select field
    categories_query = db.session.query(Category).all()
    categories = [
        (category.category_name, category.category_name)
        for category in categories_query
    ]
    form = AddProductForm()
    form.categories.choices = categories
    if form.validate_on_submit():
        product_name = form.product_name.data
        sku = form.sku.data
        product_price = form.product_price.data
        product_quantity = form.product_quantity.data
        product_description = form.product_description.data
        product_image = save_product_image(
            form.product_image.data, form.product_name.data
        )
        # make a list of categories from form
        added_categories = [
            db.session.query(Category).filter_by(category_name=category).first()
            for category in form.categories.data
        ]
        # must have category in product when add new product
        # to Product table because it has a relastionship with
        # Category tabele
        product = Product(
            product_name=product_name,
            sku=sku,
            product_price=product_price,
            quantity=product_quantity,
            product_description=product_description,
            product_image=product_image,
            # category=category,
        )
        db.session.add(product)

        # add product to each category from form
        for category in added_categories:
            category.products.append(product)
        db.session.commit()
        logger.info("Added product success.")
        flash(_(f"Add product {product.product_name} success."), "success")
        return redirect(url_for("products.add_product"))
    return render_template(
        "product/add_product.html",
        title=_("Add Product"),
        form=form,
        categories=categories_query,
    )


@products.route(
    "/admin/products/<int:product_id>/update", methods=("GET", "POST")
)
def update_product(product_id: t.Optional[int]):
    """Update informations of product with product_id. Only for superuser."""

    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("admin", "superuser"):
            abort(403)

    product = db.session.query(Product).get_or_404(product_id)
    categories_query = db.session.query(Category).all()
    categories = [(c.category_name, c.category_name) for c in categories_query]
    form = UpdateProductForm()
    form.categories.choices = categories
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.sku = form.sku.data
        product.product_price = form.product_price.data
        product.discounted_price = form.product_discounted_price.data
        product.product_quantity = form.product_quantity.data
        product.product_description = form.product_description.data
        if form.product_image.data:
            product.product_image = save_product_image(
                form.product_image.data, form.product_name.data
            )
        # first. update the new informations of product except categoies field
        db.session.commit()
        # then. update product to each categories of categories form
        # a list of categories of product after updated
        updated_categories = [
            db.session.query(Category).filter_by(category_name=category).first()
            for category in form.categories.data
        ]
        # add new category to product
        for category in updated_categories:
            # check if updated category exists in product categories
            if category in product.categories:
                continue
            # add new product to each new category
            category.products.append(product)
        db.session.commit()
        logger.info("Updated product success.")
        flash(_(f"Product {product.product_name} has been updated."), "success")
        return redirect(url_for("home.index"))
    elif request.method == "GET":
        form.product_name.data = product.product_name
        form.sku.data = product.sku
        form.product_price.data = product.product_price
        form.product_discounted_price.data = product.discounted_price
        form.product_quantity.data = product.quantity
        form.product_description.data = product.product_description
        # display categories data of product
        form.categories.data = product.categories
        return render_template(
            "product/update_product.html",
            title=_(f"Update product {product.product_name}"),
            form=form,
            product_id=product_id,
            categories=categories_query,
        )
    return redirect(url_for("home.index"))


@products.route("/products/<int:product_id>/detail", methods=("GET", "POST"))
def detail_product(product_id: t.Optional[str]):
    """Get informations of particular product by product_id."""

    product = db.session.query(Product).get_or_404(product_id)
    categories = db.session.query(Category).all()
    logger.info("Sent product info.")
    return render_template(
        "product/detail_product.html",
        title=_(f"Product {product.product_name} detail"),
        product=product,
        categories=categories,
    )


@products.route(
    "/admin/products/<int:product_id>/delete", methods=("GET", "POST")
)
def delete_product(product_id: t.Optional[int]):
    """Delete a particular product by product_id. Only superuser can do that."""

    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("admin", "superuser"):
            abort(403)
    product = db.session.query(Product).get_or_404(product_id)
    # remove product picture
    pic_path = (
        Path(current_app.root_path)
        .joinpath("static/assets/products")
        .joinpath(product.product_image)
        .resolve()
    )
    os.remove(pic_path)

    # then delete product in database
    db.session.delete(product)
    db.session.commit()
    logger.info(f"Remove product {product.product_name} success.")

    flash(_(f"This product {product_id} has been deleted."), "success")
    return redirect(url_for("home.index"))
