from django.contrib import admin

# Register your models here.
from .models import Employee, Material, MaterialRequest, MaterialRequestSignature, Project,OrganizationUnit

admin.site.register(Project)
admin.site.register(OrganizationUnit)
admin.site.register(Employee)
admin.site.register(Material)
admin.site.register(MaterialRequest)
admin.site.register(MaterialRequestSignature)