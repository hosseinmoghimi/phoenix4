from authentication.serilizers import ProfileSerializer
from django.db.models import fields
from messenger.models import Channel, Member, Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields=['id','title','body']
        
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields=['id','name','key','cluster']
class MemberSerializer(serializers.ModelSerializer):
    channel=ChannelSerializer()
    profile=ProfileSerializer()
    class Meta:
        model = Member
        fields=['id','event','profile','channel']