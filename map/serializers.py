from core import serializers as CoreSerializers
from .models import Location
class LocationSerializer(CoreSerializers.serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['id','longitude','latitude','title']