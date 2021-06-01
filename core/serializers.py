from rest_framework import serializers
from .models import BasicPage, PageLink

class BasicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPage
        fields=['id','title','get_absolute_url','thumbnail','short_description','get_edit_url']
class PageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageLink
        fields=['id','title','url','get_edit_url']
