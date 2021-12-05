
from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from .models import ResumeCategory,Resume



class ResumeCategorySerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model =ResumeCategory
        fields=['id','title','get_absolute_url','profile']