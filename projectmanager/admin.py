from django.contrib import admin

# Register your models here.
from .models import Project,OrganizationUnit

admin.site.register(Project)
admin.site.register(OrganizationUnit)