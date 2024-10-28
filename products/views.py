from rest_framework import permissions, viewsets
from rest_framework.decorators import permission_classes

from products.models import Comment, ProductCategory, Product
from products.permissions import IsSellerOrAdmin, IsUserOrReadOnly
from products.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
)


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list and retrieve product category
    """

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """

    queryset = Product.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'update', 'parital_update', 'destroy'):
            return ProductWriteSerializer

        return ProductReadSerializer

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsSellerOrAdmin,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD comments for particular product.
    """

    queryset = Comment.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        product_id = self.kwargs.get('product_id')
        return res.filter(product__id=product_id)

    def get_serializer(self, *args, **kwargs):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return CommentWriteSerializer
        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsUserOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        return super().get_permissions()
