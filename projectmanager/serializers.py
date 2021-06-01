from rest_framework import serializers
from .models import Material, Project,OrganizationUnit


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','get_absolute_url','get_edit_url','short_description','thumbnail']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Material
        fields=['id','title','get_absolute_url','get_edit_url','short_description','thumbnail']


class OrganizationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrganizationUnit
        fields=['id','title','get_absolute_url','get_edit_url','short_description','thumbnail']