from django.contrib import admin

from salary.models import Attendance, EmployeeSalary, SalaryLine, Vacation, WorkDay, WorkGroup, WorkSite


admin.site.register(EmployeeSalary)
admin.site.register(SalaryLine)
admin.site.register(WorkDay)
admin.site.register(WorkGroup)
admin.site.register(Attendance)
admin.site.register(WorkSite)
admin.site.register(Vacation)