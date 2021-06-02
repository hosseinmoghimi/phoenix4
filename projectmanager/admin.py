from django.contrib import admin

# Register your models here.
from .models import Employee, EmployeeSpeciality, Employer, Material, MaterialRequest, MaterialRequestSignature, Project,OrganizationUnit

admin.site.register(Project)
admin.site.register(OrganizationUnit)
admin.site.register(EmployeeSpeciality)
admin.site.register(Employee)
admin.site.register(Material)
admin.site.register(MaterialRequest)
admin.site.register(MaterialRequestSignature)
admin.site.register(Employer)