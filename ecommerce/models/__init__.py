"""
This package contain all models of the app and more add-on includes
"""

from ecommerce.search import SearchableMixin
from ecommerce.models.user import *
from ecommerce.models.product import *
from ecommerce.models.role import *
from ecommerce.models.cart import *
from ecommerce.models.category import *
from ecommerce.models.order import *
from ecommerce.models.ordered_product import *
from ecommerce.models.sale_transaction import *


# elasticsearch config
db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
