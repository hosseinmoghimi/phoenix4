from .models import *
from core import enums as CoreEnums
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
        
class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model=Farm
        fields=['id','name','get_absolute_url']

        
class SaloonSerializer(serializers.ModelSerializer):
    farm=FarmSerializer()
    class Meta:
        model=Saloon
        fields=['id','farm','name','get_absolute_url']

class AnimalSerializer(serializers.ModelSerializer):
    current_in_saloon=SaloonSerializer()
    class Meta:
        model=Animal
        fields=['id','current_in_saloon','name','tag','weight','price','persian_enter_date','category','image','get_absolute_url','get_edit_url']



        
   
class EmployeeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Saloon
        fields=['id','profile','get_absolute_url']


class AnimalInSaloonSerializer(serializers.ModelSerializer):
    animal=AnimalSerializer()
    saloon=SaloonSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=AnimalInSaloon
        fields=['id','animal','employee','animal_weight','animal_price','saloon','persian_enter_date','persian_exit_date','get_edit_url']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food
        fields=['id','title','unit_name','unit_price','get_absolute_url']
class KoshtarSerializer(serializers.ModelSerializer):
    animal=AnimalSerializer()
    class Meta:
        model=Koshtar
        fields=['id','animal','Jegar_price','Kalle_pache_price',
        'pust_price','transport_fee','koshtar_fee',
        'lashe_price','lashe_weight','description',
        'get_edit_url','get_absolute_url']

class CostSerializer(serializers.ModelSerializer):
    saloon=SaloonSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=Cost
        fields=['id','saloon','title','persian_cost_date','category','employee','value','get_absolute_url']

class SaloonFoodSerializer(serializers.ModelSerializer):
    food=FoodSerializer()
    saloon=SaloonSerializer()
    class Meta:
        model=SaloonFood
        fields=['id','food','saloon','unit_name','quantity','unit_price']

