from django.db.models import fields
from salary.models import EmployeeSalary
from projectmanager.serializers import EmployeeSerializer
from .apps import APP_NAME
from rest_framework import serializers

class EmployeeSalarySerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=EmployeeSalary
        fields=['id','employee','year','month']