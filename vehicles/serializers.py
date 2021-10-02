from core import serializers as CoreSerializers
from .models import Vehicle,VehicleWorkEvent,Maintenance,WorkShift,ServiceMan,Driver
class VehicleSerializer(CoreSerializers.serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['id','name','brand','model_name','vehicle_type','owner','get_absolute_url']
class DriverSerializer(CoreSerializers.serializers.ModelSerializer):
    profile=CoreSerializers.ProfileSerializer()
    class Meta:
        model=Driver
        fields=['id','profile','get_absolute_url']
class WorkShiftSerializer(CoreSerializers.serializers.ModelSerializer):
    driver=DriverSerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=WorkShift
        fields=['id','vehicle','income','outcome','driver','persian_start_time','persian_end_time']
class ServiceManSerializer(CoreSerializers.serializers.ModelSerializer):
    profile=CoreSerializers.ProfileSerializer()
    class Meta:
        model=ServiceMan
        fields=['id','name','profile','get_absolute_url']
class MaintenanceSerializer(CoreSerializers.serializers.ModelSerializer):
    service_man=ServiceManSerializer()
    vehicle=VehicleSerializer()
    class Meta:
        model=Maintenance
        fields=['id','maintenance_type','service_man','vehicle','get_absolute_url','persian_event_time']
class VehicleWorkEventSerializer(CoreSerializers.serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    work_shift=WorkShiftSerializer()
    class Meta:
        model=VehicleWorkEvent
        fields=['id','vehicle','event_type','work_shift','get_absolute_url','persian_event_time']