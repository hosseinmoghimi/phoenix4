from rest_framework import serializers
from .models import Employee, Employer, Event, Material, MaterialRequest, MaterialRequestSignature, Project,OrganizationUnit, ProjectLocation, Service, ServiceRequest, ServiceRequestSignature
from authentication.serilizers import ProfileSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','full_title','get_absolute_url','get_edit_url','short_description','thumbnail','persian_start_date','persian_end_date','percentage_completed']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Material
        fields=['id','title','full_title','get_absolute_url','unit_price','unit_name','get_edit_url','short_description','thumbnail']


class EmployerSerializer(serializers.ModelSerializer):

    class Meta:
        model=Employer
        fields=['id','title','image','pre_title','get_edit_url','get_absolute_url']






class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model=Service
        fields=['id','title','unit_name','unit_price','thumbnail','get_absolute_url']


class MaterialRequestSerializer(serializers.ModelSerializer):
    material=MaterialSerializer()
    project=ProjectSerializer()
    profile=ProfileSerializer()
    class Meta:
        model=MaterialRequest
        fields=['id','material','quantity','persian_date_added','get_edit_url','get_status_tag','project','profile','unit_name','unit_price','get_absolute_url']

class EmployeeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Employee
        fields=['id','get_absolute_url','profile']

class ServiceRequestSerializer(serializers.ModelSerializer):
    service=ServiceSerializer()
    employee=EmployeeSerializer()
    project=ProjectSerializer()
    profile=ProfileSerializer()
    class Meta:
        model=ServiceRequest
        fields=['id','service','employee','quantity','persian_date_added','get_edit_url','get_status_tag','project','profile','unit_name','unit_price','get_absolute_url']
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','title','get_absolute_url','persian_event_datetime']
class ProjectLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectLocation
        fields=['id','location','title','get_edit_url','get_project_url','project_title']

class OrganizationUnitSerializer(serializers.ModelSerializer):
    employees=EmployeeSerializer(many=True)
    employer=EmployerSerializer()
    class Meta:
        model=OrganizationUnit
        fields=['id','employer','title','employees','get_absolute_url','get_edit_url','short_description','thumbnail']
class MaterialRequestSignatureSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=MaterialRequestSignature
        fields=['id','status','profile','get_edit_url','description','persian_date_added','get_status_color']

class ServiceRequestSignatureSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=ServiceRequestSignature
        fields=['id','status','profile','get_edit_url','description','persian_date_added','get_status_color']