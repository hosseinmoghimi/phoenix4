from django.contrib import admin

from salary.models import EmployeeSalary, SalaryLine


admin.site.register(EmployeeSalary)
admin.site.register(SalaryLine)