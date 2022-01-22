from rest_framework import serializers
from .models import Blog, CryptoToken,OurTeam
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title','thumbnail','get_absolute_url','short_description']


class CryptoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoToken
        fields = ['id','title','thumbnail','get_absolute_url','short_description']
