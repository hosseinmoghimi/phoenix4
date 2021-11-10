from rest_framework import serializers
from .models import Book
from authentication.serializers import ProfileSerializer


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model=Book
        fields=['id','title','get_edit_url','get_absolute_url']

