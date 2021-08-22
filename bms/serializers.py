from core import serializers as CoreSerializers
from rest_framework import serializers
from .models import *

class FeederSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feeder
        fields=['id','name','ip','port','pin','thumbnail','serial_no']

class RelaySerializerForExportData(serializers.ModelSerializer):
    class Meta:
        model=Relay
        fields=['id','name','feeder_id','register','current_state','enabled','get_absolute_url','pin']

class RelaySerializer(serializers.ModelSerializer):
    feeder=FeederSerializer()
    class Meta:
        model=Relay
        fields=['id','name','feeder_id','feeder','register','current_state','enabled','get_absolute_url','pin']

class CommandSerializer(serializers.ModelSerializer):
    relay=RelaySerializer()
    profiles=CoreSerializers.ProfileSerializer(many=True)
    class Meta:
        model=Command
        fields=['id','name','relay_id','iteration','profiles','value','color','relay','get_absolute_url']
class CommandSerializerForExportData(serializers.ModelSerializer):
    class Meta:
        model=Command
        fields=['id','name','relay_id','iteration','value','color','get_absolute_url']

class CommandSerializerForScenario(serializers.ModelSerializer):
    class Meta:
        model=Command
        fields=['id']


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Scenario    
        fields=['id','name','get_absolute_url','pin']
        

class ScenarioSerializerForExportData(serializers.ModelSerializer):
    commands=CommandSerializerForScenario(many=True)
    class Meta:
        model=Scenario    
        fields=['id','name','get_absolute_url','commands','pin']
        

class ScenarioSerializerForLog(serializers.ModelSerializer):
    class Meta:
        model=Scenario    
        fields=['id','name','get_absolute_url']
class RelaySerializerForLog(serializers.ModelSerializer):
    class Meta:
        model=Relay    
        fields=['id','name','get_absolute_url']
class FeederSerializerForLog(serializers.ModelSerializer):
    class Meta:
        model=Feeder
        fields=['id','name','get_absolute_url']
class CommandSerializerForLog(serializers.ModelSerializer):
    class Meta:
        model=Command
        fields=['id','name','get_absolute_url']
class LogSerializer(serializers.ModelSerializer):
    feeder=FeederSerializerForLog()
    command=CommandSerializerForLog()
    scenario=ScenarioSerializerForLog()
    profile=CoreSerializers.ProfileSerializer()
    relay=RelaySerializerForLog()
    class Meta:
        model=Log
        fields=['id','title','succeed','profile','relay','feeder','command','scenario','persian_date_added']
        