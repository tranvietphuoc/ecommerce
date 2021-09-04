from flask import (
    Blueprint,
    abort,
    flash,
    render_template,
    redirect,
    url_for,
    request,
)
from ..models import db, Category
from flask_login import current_user
from .forms import (
    AddCategoryForm,
    UpdateCategoryForm,
)
from flask_babel import _


categories = Blueprint("categories", __name__)


@categories.route("/admin/categories/new", methods=("GET", "POST"))
def add_category():
    """Add new category. Only superuser can do that."""

    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("admin", "superuser"):
            abort(403)
    cates = db.session.query(Category).all()
    form = AddCategoryForm()
    if form.validate_on_submit():
        category_name = form.category_name.data
        db.session.add(Category(category_name=category_name))
        db.session.commit()
        flash(_(f"Add category {category_name} success."), "success")
        return redirect(url_for("categories.add_category"))
    return render_template(
        "category/add_category.html",
        title=_("Add Category"),
        form=form,
        cates=cates,
    )


@categories.route(
    "/admin/categories/<int:category_id>/update", methods=("GET", "POST")
)
def update_category(category_id):
    """Update informations of category has category_id. Only for superuser."""

    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("admin", "superuser"):
            abort(403)
    categories = db.session.query(Category).all()
    category = db.session.query(Category).get_or_404(category_id)
    form = UpdateCategoryForm()
    if form.validate_on_submit():
        category.category_name = form.category_name.data
        category.products.append()
        db.session.commit()
        flash(
            _(f"Category {category.category_name} has been updated."), "success"
        )
        return redirect(url_for("categories.get_category"))
    elif request.method == "GET":
        form.category_name.data = category.category_name
        return render_template(
            "category/update_category.html",
            title=_(f"Update category {category.category_name}"),
            form=form,
            categories=categories,
        )
    return redirect(url_for("categories.get_categories"))


@categories.route(
    "/categories/<int:category_id>/detail", methods=("GET", "POST")
)
def detail_category(category_id):
    """Get details of category with category_id (display category and all products of it)"""

    # need to join between Product and Category table
    result = db.session.query(Category).get_or_404(category_id)
    categories = db.session.query(Category).all()
    return render_template(
        "category/detail_category.html",
        title=_(f"Category {result.category_name} detail"),
        result=result,
        categories=categories,
    )


@categories.route("/categories/list", methods=("GET", "POST"))
def get_categories():
    """Get all categories. And show the informations of them."""

    cates = db.session.query(Category).all()
    return render_template(
        "category/get_categories.html",
        title=_("List categories"),
        cates=cates,
    )


@categories.route(
    "/admin/categories/<int:category_id>/delete", methods=("GET", "POST")
)
def delete_category(category_id):
    """Delete particular category with category_id. Only superuser can delete."""

    if not current_user.is_active or not current_user.is_authenticated:
        abort(404)
    else:
        if not current_user.has_role("admin", "superuser"):
            abort(403)
    category = db.session.query(Category).get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(_(f"The category {category_id} has been deleted."), "success")
    return redirect(url_for("home.index"))
