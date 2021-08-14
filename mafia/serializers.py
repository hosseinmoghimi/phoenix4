from rest_framework import serializers
from .models import Player,Game,God, Role
from authentication.serilizers import ProfileSerializer

class PlayerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Player
        fields=['id','profile','bio','score','get_absolute_url','image','name']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields=['id','role_name','description','default_count','side']
