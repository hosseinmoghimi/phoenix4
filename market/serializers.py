from .models import Category, Product
from rest_framework import serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','thumbnail','get_absolute_url']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','get_absolute_url','thumbnail']