from .models import Category, Product
from rest_framework import fields, serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','get_absolute_url','thumbnail']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','get_absolute_url','thumbnail']