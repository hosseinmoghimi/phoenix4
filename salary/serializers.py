from django.db.models import fields
from salary.models import EmployeeSalary, SalaryLine, Vacation
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
class VacationSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=Vacation
        fields=['id','title','employee','persian_vacation_started','persian_vacation_ended','description','get_edit_url','get_absolute_url']