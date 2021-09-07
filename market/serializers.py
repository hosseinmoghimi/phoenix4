from .models import CartLine, Category, Product, Shop
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'thumbnail', 'get_absolute_url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'get_absolute_url', 'thumbnail']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'supplier_id','product_id', 'unit_name', 'available', 'unit_price']


class CartLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartLine
        fields = ['id','quantity']
