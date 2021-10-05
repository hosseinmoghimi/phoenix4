from rest_framework import serializers
from .models import Employee, Employer, Event, Material, MaterialRequest, RequestSignature, Project,OrganizationUnit, Location, Service, ServiceRequest, WareHouseSheet
from authentication.serializers import ProfileSerializer


class EmployerSerializer(serializers.ModelSerializer):

    class Meta:
        model=Employer
        fields=['id','title','image','pre_title','get_edit_url','get_absolute_url']


class ProjectSerializer(serializers.ModelSerializer):
    employer=EmployerSerializer()
    contractor=EmployerSerializer()
    class Meta:
        model=Project
        fields=['id','title','get_status_color','employer','contractor','full_title','status','sum_total','get_absolute_url','get_edit_url','short_description','thumbnail','persian_start_date','persian_end_date','percentage_completed']

class ProjectSerializerForGuantt(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','get_status_color','start_date','end_date','status','sum_total','get_absolute_url','short_description','thumbnail','percentage_completed']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Material
        fields=['id','title','full_title','get_absolute_url','unit_price','unit_name','get_edit_url','short_description','thumbnail']





class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model=Service
        fields=['id','title','unit_name','unit_price','thumbnail','get_absolute_url']


class EmployeeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Employee
        fields=['id','get_absolute_url','profile']
class MaterialRequestSerializer(serializers.ModelSerializer):
    material=MaterialSerializer()
    project=ProjectSerializer()
    handler=EmployeeSerializer()
    class Meta:
        model=MaterialRequest
        fields=['id','material','quantity','persian_date_added','get_edit_url','get_status_tag','project','handler','unit_name','unit_price','get_absolute_url']

class EventSerializerForChart(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','title','get_absolute_url','start_datetime2','end_datetime2']

class ServiceRequestSerializer(serializers.ModelSerializer):
    service=ServiceSerializer()
    project=ProjectSerializer()
    handler=EmployeeSerializer()
    class Meta:
        model=ServiceRequest
        fields=['id','service','handler','quantity','persian_date_added','get_edit_url','get_status_tag','project','unit_name','unit_price','get_absolute_url']
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','title','get_absolute_url','persian_event_datetime','persian_start_datetime','persian_end_datetime','start_datetime','end_datetime']
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Location
        fields=['id','location','title','get_edit_url','get_absolute_url']

class OrganizationUnitSerializer(serializers.ModelSerializer):
    employees=EmployeeSerializer(many=True)
    employer=EmployerSerializer()
    class Meta:
        model=OrganizationUnit
        fields=['id','employer','title','employees','get_absolute_url','get_edit_url','short_description','thumbnail']
class RequestSignatureSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=RequestSignature
        fields=['id','status','employee','get_edit_url','description','persian_date_added','get_status_color']


class WareHouseSheetSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    material=MaterialSerializer()
    class Meta:
        model=WareHouseSheet
        fields=['id','direction','material','employee','get_edit_url','description','persian_date_added','get_status_color','get_absolute_url']

