from django.contrib import admin

# Register your models here.
from .models import Employee, EmployeeSpeciality, Employer, Event, Material, MaterialRequest, MaterialRequestSignature, Project,OrganizationUnit, Location, Request, RequestSignature, Service, ServiceRequest, ServiceRequestSignature

admin.site.register(Location)
admin.site.register(Request)
admin.site.register(RequestSignature)
admin.site.register(Project)
admin.site.register(OrganizationUnit)
admin.site.register(EmployeeSpeciality)
admin.site.register(Employee)
admin.site.register(Material)
admin.site.register(Event)
admin.site.register(MaterialRequest)
admin.site.register(MaterialRequestSignature)
admin.site.register(ServiceRequestSignature)
admin.site.register(ServiceRequest)
admin.site.register(Service)
admin.site.register(Employer)