from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import ProductCategoryViewSet, ProductViewSet, CommentViewSet

app_name = 'products'

router = DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'', ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
