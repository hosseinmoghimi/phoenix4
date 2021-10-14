from .apps import APP_NAME
from django import forms

class AddEmployeeSalaryForm(forms.Form):
    employee_id=forms.IntegerField(required=True)
    year=forms.IntegerField(required=True)
    month=forms.IntegerField(required=False)
    month_name=forms.CharField( max_length=20, required=False)
    description=forms.CharField( max_length=2000, required=False)

class AddSalaryLineForm(forms.Form):
    employee_salary_id=forms.IntegerField(required=True)
    direction=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    title=forms.CharField(max_length=500,required=True)
    description=forms.CharField( max_length=2000, required=False)