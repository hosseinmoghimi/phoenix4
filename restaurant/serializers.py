from authentication.serializers import ProfileSerializer
from .models import Food, Guest, Meal
from rest_framework import serializers

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields=['id','title' ,'get_edit_url','get_absolute_url']
class MealSerializer(serializers.ModelSerializer):
    food=FoodSerializer()
    class Meta:
        model=Meal
        fields=['id','food' ,'persian_date_served','get_edit_url','get_absolute_url','meal_type']

class GuestSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Guest
        fields=['id','profile','get_absolute_url']