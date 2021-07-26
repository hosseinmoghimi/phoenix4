from .models import *
from core import enums as CoreEnums
from rest_framework import serializers

        
class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Animal
        fields=['id','name','tag','weight','price','persian_enter_date','category','image','get_absolute_url']



        
class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model=Farm
        fields=['id','name','get_absolute_url']

        
class SaloonSerializer(serializers.ModelSerializer):
    farm=FarmSerializer()
    class Meta:
        model=Saloon
        fields=['id','farm','name','get_absolute_url']


class AnimalInSaloonSerializer(serializers.ModelSerializer):
    animal=AnimalSerializer()
    saloon=SaloonSerializer()
    class Meta:
        model=AnimalInSaloon
        fields=['id','animal','animal_weight','animal_price','saloon','persian_enter_date','persian_exit_date']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields=['id','title','unit_name','unit_price','get_absolute_url']

class SaloonFoodSerializer(serializers.ModelSerializer):
    food=FoodSerializer()
    saloon=SaloonSerializer()
    class Meta:
        model=SaloonFood
        fields=['id','food','saloon','unit_name','quantity','unit_price']

