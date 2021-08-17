from rest_framework import serializers
from .models import GameRole, Player,Game,God, Role
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

class GameRoleSerializer(serializers.ModelSerializer):
    role=RoleSerializer()
    player=PlayerSerializer()
    class Meta:
        model = GameRole
        fields=['id','role','player','turn','get_absolute_url']
