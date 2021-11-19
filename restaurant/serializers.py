from .models import Food
from rest_framework import serializers

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields=['id','title' ,'get_edit_url','get_absolute_url']