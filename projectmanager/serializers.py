from authentication.repo import ProfileRepo
from rest_framework import serializers
from .models import Material, MaterialRequest, Project,OrganizationUnit
from authentication.serilizers import ProfileSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','get_absolute_url','get_edit_url','short_description','thumbnail']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Material
        fields=['id','title','get_absolute_url','unit_price','unit_name','get_edit_url','short_description','thumbnail']


class MaterialRequestSerializer(serializers.ModelSerializer):
    material=MaterialSerializer()
    project=ProjectSerializer()
    profile=ProfileSerializer()
    class Meta:
        model=MaterialRequest
        fields=['id','material','quantity','get_edit_url','get_status_tag','project','profile','unit_name','unit_price','get_absolute_url']


class OrganizationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrganizationUnit
        fields=['id','title','get_absolute_url','get_edit_url','short_description','thumbnail']