from .apps import APP_NAME
from django import forms

class AddEmployeeSalaryForm(forms.Form):
    employee_id=forms.IntegerField(required=True)
    year=forms.IntegerField(required=True)
    month=forms.IntegerField(required=False)
    month_name=forms.CharField( max_length=20, required=False)