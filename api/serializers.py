from rest_framework import serializers
from .models import Category, Product, ProductImage, UserPersonalCart, CartItem


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'src',)


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = Category()
        category.name = validated_data.get('name')
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()
    rating = serializers.FloatField()

    def create(self, validated_data):
        product = Product()
        product.name = validated_data.get('name')
        product.price = validated_data.get('price')
        product.category_id = validated_data.get('category_id')
        product.rating = validated_data.get('rating')
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.price = validated_data.get('price')
        instance.category_id = validated_data.get('category_id')
        instance.rating = validated_data.get('rating')
        instance.save()
        return instance


class CartItemCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'total_price')


class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = UserPersonalCart
        fields = ('items', 'total_price')
