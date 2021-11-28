from rest_framework import serializers
from .models import ResumeSkill

class ResumeSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResumeSkill
        fields=['id','title','percentage']