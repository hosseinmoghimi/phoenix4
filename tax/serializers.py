from rest_framework import serializers
from .models import Tax
from authentication.serializers import ProfileSerializer


class TaxSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tax
        fields=['id','title','amount','year','get_edit_url','get_absolute_url']

