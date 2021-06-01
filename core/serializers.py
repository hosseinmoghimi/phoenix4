from rest_framework import serializers
from .models import BasicPage

class BasicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPage
        fields=['id','title','get_absolute_url','thumbnail','short_description','get_edit_url']
