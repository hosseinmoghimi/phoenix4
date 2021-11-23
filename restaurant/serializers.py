from authentication.serializers import ProfileSerializer
from .models import Food, Guest, Host, Meal, ReservedMeal
from rest_framework import serializers

class GuestSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Guest
        fields=['id','profile','get_absolute_url']
class HostSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Host
        fields=['id','profile','title','get_absolute_url','get_edit_url']
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields=['id','title' ,'get_edit_url','get_absolute_url']
class MealSerializer(serializers.ModelSerializer):
    foods=FoodSerializer(many=True)
    host=HostSerializer()
    class Meta:
        model=Meal
        fields=['id','title','foods','host' ,'reserved','reserves_count','persian_date_served','get_edit_url','get_absolute_url','meal_type']

class ReservedMealSerializer(serializers.ModelSerializer):
    meal=MealSerializer()
    guest=GuestSerializer()
    class Meta:
        model=ReservedMeal
        fields=['id','meal','quantity','guest' ,'persian_date_served','get_edit_url','get_absolute_url']
