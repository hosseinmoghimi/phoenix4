from django.db.models import fields
from messenger.models import Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields=['id','title','get_absolute_url']