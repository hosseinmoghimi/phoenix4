from rest_framework import serializers
from .models import Appointment
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointment
        fields=['id,.title','get_absolute_url','get_edit_url']