from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def category_image_path(instance, filename):
    return f'products/category/icons/{instance.name}/{filename}'


def products_image_path(instance, filename):
    return f'products/images/{instance.name}/{filename}'


class ProductCategory(models.Model):
    name = models.CharField(_('Category name'), max_length=120)
    icon = models.ImageField(upload_to=category_image_path, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    def __str__(self):
        return self.name


def get_default_product_category():
    return ProductCategory.objects.get_or_create(name='Other')[0]


class Product(models.Model):
    seller = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(
        ProductCategory,
        related_name='product_list',
        on_delete=models.SET(get_default_product_category),
    )

    name = models.CharField(max_length=120)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to=products_image_path, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(
        Product, related_name='comments', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name='products_comments', null=True, on_delete=models.SET_NULL
    )

    body = models.TextField(_('Comment body'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.body[:20]} by {self.user.username}'
