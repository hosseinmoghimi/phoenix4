from django import forms
from django.forms.fields import IntegerField

class AddWorkShiftForm(forms.Form):
    vehicle_id=forms.IntegerField(required=True)
    start_date=forms.CharField( max_length=50, required=True)
    end_date=forms.CharField( max_length=50, required=True)
    driver_id=forms.IntegerField( required=True)
    