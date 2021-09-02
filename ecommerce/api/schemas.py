from ecommerce.models import (
    User,
    Product,
    Category,
    Role,
    Order,
    OrderedProduct,
    SaleTransaction,
    Cart,
)
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        include_relationships = True


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True
        include_relationships = True

    date_created = auto_field(dump_only=True)


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True
        include_relationships = True

    date_added = auto_field(dump_only=True)


class OrderShema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order


class OrderedProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderedProduct


class CartSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cart


class SaleTransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SaleTransaction
