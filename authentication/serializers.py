from .models import MembershipRequest, Profile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','name','first_name','last_name','mobile','address','email','image','get_absolute_url','bio']

class MembershipRequestSerializer(serializers.ModelSerializer):
    handled_by=ProfileSerializer()
    class Meta:
        model=MembershipRequest
        fields=['id','handled_by','mobile','read','app_name','get_delete_url','handled','persian_date_added','persian_date_handled']
