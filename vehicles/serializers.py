from rest_framework import serializers
from .models import Area, Vehicle,VehicleWorkEvent,Maintenance,WorkShift,ServiceMan,Driver
from authentication.serializers import ProfileSerializer

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['id','name','brand','model_name','vehicle_type','owner','get_absolute_url']

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=['id','code','name','get_absolute_url']

class DriverSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Driver
        fields=['id','profile','get_absolute_url']


class WorkShiftSerializer(serializers.ModelSerializer):
    driver=DriverSerializer()
    vehicle=VehicleSerializer()
    area=AreaSerializer()
    class Meta:
        model=WorkShift
        fields=['id','vehicle','income','outcome','driver','persian_start_time','persian_end_time','area','get_absolute_url','get_edit_url']


class ServiceManSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=ServiceMan
        fields=['id','name','profile','get_absolute_url']


class MaintenanceSerializer(serializers.ModelSerializer):
    service_man=ServiceManSerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=Maintenance
        fields=['id','maintenance_type','get_edit_url','kilometer','service_man','paid','vehicle','get_absolute_url','persian_event_datetime']


class VehicleWorkEventSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    work_shift=WorkShiftSerializer()
    class Meta:
        model=VehicleWorkEvent
        fields=['id','vehicle','event_type','work_shift','get_absolute_url','persian_event_datetime']

