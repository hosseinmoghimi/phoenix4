from django import forms
from django.forms.fields import IntegerField

class AddWorkShiftForm(forms.Form):
    vehicle_id=forms.IntegerField(required=True)
    start_datetime=forms.CharField( max_length=50, required=True)
    end_datetime=forms.CharField( max_length=50, required=True)
    driver_id=forms.IntegerField( required=True)
    area_id=forms.IntegerField( required=True)
    income=forms.IntegerField( required=True)
    outcome=forms.IntegerField( required=True)
    description=forms.CharField( max_length=5000, required=False)

class AddMaintenanceForm(forms.Form):
    vehicle_id=forms.IntegerField(required=True)
    service_man_id=forms.IntegerField(required=False)
    event_datetime=forms.CharField( max_length=25, required=True)
    title=forms.CharField( max_length=100, required=True)
    description=forms.CharField( max_length=5000, required=False)
    paid=forms.IntegerField(required=True)
    maintenance_type=forms.CharField( max_length=100, required=False)
    kilometer=forms.IntegerField( required=False)

class AddVehicleForm(forms.Form):
    name=forms.CharField( max_length=100, required=True)
    

class AddTripForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)

class AddVehicleWorkEventForm(forms.Form):
    work_shift_id=forms.IntegerField(required=True)
    event_type=forms.CharField( max_length=50, required=True)
    vehicle_id=forms.IntegerField(required=True)
    event_datetime=forms.CharField( max_length=50, required=True)
    kilometer=forms.IntegerField( required=True)
     
    description=forms.CharField( max_length=5000, required=False)

    
