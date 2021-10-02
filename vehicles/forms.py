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
    description=forms.CharField( max_length=50, required=False)
