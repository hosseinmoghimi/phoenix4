from rest_framework import serializers
from .models import Player,Game,God
from authentication.serilizers import ProfileSerializer

class PlayerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Player
        fields=['id','profile','bio','score','get_absolute_url','image','name']
