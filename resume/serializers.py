from rest_framework import serializers
from .models import ResumeFact, ResumeSkill

class ResumeSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResumeSkill
        fields=['id','title','percentage','get_absolute_url']

class ResumeFactSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResumeFact
        fields=['id','title','count','icon','get_absolute_url','get_edit_url']