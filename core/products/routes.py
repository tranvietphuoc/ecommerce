from flask import (
    Blueprint,
    abort,
    flash,
    render_template,
    redirect,
    url_for,
    request,
)
from core.models import db, Product, Category
from flask_login import current_user
from core.products.forms import (
    AddProductForm,
    AddCategoryForm,
    UpdateCategoryForm,
    UpdateProductForm,
)
from core.products.utils import save_product_image


products = Blueprint("products", __name__)


@products.route("/products/new", methods=("GET", "POST"))
def add_product():
    """Only superuser can add products."""
    if not current_user.is_authenticated or not current_user.is_active:
        abort(404)  # login to use this function
    else:
        if not current_user.has_role("superuser"):
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
        flash(f"Add product success.", "success")
        return redirect(url_for("products.add_product"))
    return render_template("product/add_product.html", title="Add Product", form=form)


@products.route("/products/<int:product_id>/update", methods=("GET", "POST"))
def update_product(product_id):
    """Update informations of product with product_id. Only for superuser."""
    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("superuser"):
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
        print(updated_categories)
        # add new category to product
        for category in updated_categories:
            # check if updated category exists in product categories
            if category in product.categories:
                continue
            # add new product to each new category
            category.products.append(product)
        db.session.commit()
        flash(f"Product {product.product_name} has been updated.", "success")
        return redirect(url_for("main.home"))
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
            title=f"Update product {product.product_name}",
            form=form,
            product_id=product_id,
        )
    return redirect(url_for("main.home"))


@products.route("/products/<int:product_id>/detail", methods=("GET", "POST"))
def detail_product(product_id):
    """Get informations of particular product by product_id."""
    product = db.session.query(Product).get_or_404(product_id)
    return render_template(
        "product/detail_product.html",
        title=f"Product {product.product_name} detail",
        product=product,
    )


@products.route("/products/<int:product_id>/delete", methods=("GET", "POST"))
def delete_product(product_id):
    """Delete a particular product by product_id. Only superuser can do that."""
    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("superuser"):
            abort(403)
    product = db.session.query(Product).get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f"This product {product_id} has been deleted.", "success")
    return redirect(url_for("main.home"))


@products.route("/categories/new", methods=("GET", "POST"))
def add_category():
    """Add new category. Only superuser can do that."""
    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("superuser"):
            abort(403)

    form = AddCategoryForm()
    if form.validate_on_submit():
        category_name = form.category_name.data
        db.session.add(Category(category_name=category_name))
        db.session.commit()
        flash(f"Add category success.", "success")
        return redirect(url_for("products.add_category"))
    return render_template("product/add_category.html", title="Add Category", form=form)


@products.route("/categories<int:category_id>/update", methods=("GET", "POST"))
def update_category(category_id):
    """Update informations of category has category_id. Only for superuser."""
    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("superuser"):
            abort(403)

    category = db.session.query(Category).get_or_404(category_id)
    form = UpdateCategoryForm()
    if form.validate_on_submit():
        category.category_name = form.category_name.data
        category.products.append()
        db.session.commit()
        flash(f"This category has been updated.", "success")
        return redirect(url_for("products.get_category"))
    elif request.method == "GET":
        form.category_name.data = category.category_name
        return render_template(
            "product/update_category.html",
            title=f"Update category {category.category_name}",
            form=form,
        )
    return redirect(url_for("products.get_categories"))


@products.route("/categories/<int:category_id>/detail", methods=("GET", "POST"))
def detail_category(category_id):
    """Get details of category with category_id (display category and all products of it)"""
    # need to join between Product and Category table
    result = db.session.query(Category).get_or_404(category_id)
    return render_template(
        "product/detail_category.html",
        title=f"Category {result.category_name} detail",
        result=result,
    )


@products.route("/categories/list", methods=("GET", "POST"))
def get_categories():
    """Get all categories. And show the informations of them."""
    categories = db.session.query(Category).all()
    return render_template(
        "product/categories.html", title="List categories", categories=categories,
    )


@products.route("/categories/<int:category_id>/delete", methods=("GET", "POST"))
def delete_category(category_id):
    """Delete particular category with category_id. Only superuser can delete."""
    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("superuser"):
            abort(403)

    category = db.session.query(Category).get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f"The category {category_id} has been deleted.", "success")
    return redirect(url_for("main.home"))
