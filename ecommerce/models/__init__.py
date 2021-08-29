"""
This package contain all models of the app and more add-on includes
"""

from ecommerce.search import SearchableMixin
from .user import *
from .product import *
from .role import *
from .cart import *
from .category import *
from .order import *
from .ordered_product import *
from .sale_transaction import *


# elasticsearch config
db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
