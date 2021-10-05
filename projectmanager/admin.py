from django.contrib import admin

# Register your models here.
from .models import WareHouseSheet,Employee, EmployeeSpeciality, Employer, Event, Material, MaterialRequest, RequestSignature, Project,OrganizationUnit, Location, Request, RequestSignature, Service, ServiceRequest, WareHouse

admin.site.register(Location)
admin.site.register(Request)
admin.site.register(RequestSignature)
admin.site.register(Project)
admin.site.register(OrganizationUnit)
admin.site.register(EmployeeSpeciality)
admin.site.register(Employee)
admin.site.register(Material)
admin.site.register(WareHouse)
admin.site.register(WareHouseSheet)
admin.site.register(Event)
admin.site.register(MaterialRequest)
admin.site.register(ServiceRequest)
admin.site.register(Service)
admin.site.register(Employer)