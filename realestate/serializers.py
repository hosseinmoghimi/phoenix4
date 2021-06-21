from rest_framework import serializers
from .models import PropertyFeature
class PropertyFeatureSerializer(serializers.ModelSerializer):
    class Meta:        
        model = PropertyFeature
        fields=['id','name','value']