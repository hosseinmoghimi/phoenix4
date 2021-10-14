from django.db.models import fields
from salary.models import EmployeeSalary, SalaryLine
from projectmanager.serializers import EmployeeSerializer
from .apps import APP_NAME
from rest_framework import serializers

class EmployeeSalarySerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=EmployeeSalary
        fields=['id','employee','year','month','month_name','get_edit_url','get_absolute_url']
class SalaryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model=SalaryLine
        fields=['id','amount','direction','title','description','get_edit_url','get_absolute_url']