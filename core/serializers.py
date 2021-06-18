from rest_framework import serializers
from .models import BasicPage, Image, PageDocument, PageImage, PageLink

class BasicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPage
        fields=['id','title','get_absolute_url','parent_id','thumbnail','short_description','get_edit_url']
class PageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageLink
        fields=['id','title','url','get_edit_url']
class PageDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageDocument
        fields=['id','title','get_download_url','get_edit_url']
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields=['id','title','image','get_edit_url']
class PageImageSerializer(serializers.ModelSerializer):
    image=ImageSerializer()
    class Meta:
        model = PageImage
        fields=['id','image']