from rest_framework import serializers
from products.models import Comment, Product, ProductCategory


class ProductCategoryReadSerializer(serializers.ModelSerializer):
    """
    serializer class for product categories
    """

    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductReadSerializer(serializers.ModelSerializer):
    """
    serializer class for reading products
    """

    seller = serializers.CharField(source='seller.get_full_name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    serializer class for writing products
    """

    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = ProductCategoryReadSerializer()

    class Meta:
        model = Product
        fields = (
            'seller',
            'category',
            'name',
            'desc',
            'image',
            'price',
            'quantity',
        )

    def create(self, validated_data):
        category = validated_data.pop('category')
        instance, created = ProductCategory.objects.get_or_create(**category)
        product = Product.objects.create(**validated_data, category=instance)

        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            nested_serializer = self.fields['category']
            nested_instance = instance.category
            nested_data = validated_data.pop('category')
            nested_serializer.update(nested_instance, nested_data)

        return super(ProductWriteSerializer, self).update(instance, validated_data)


class CommentReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
