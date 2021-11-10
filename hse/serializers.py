from rest_framework import serializers
from .models import Blog
from authentication.serializers import ProfileSerializer


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model=Blog
        fields=['id','title','get_edit_url','get_absolute_url']

