from django.contrib import admin

# Register your models here.
from .models import EmployeeDocument, WareHouseExportSheet, WareHouseImportSheet, WareHouseMaterial, WareHouseSheet,Employee, EmployeeSpeciality, Employer, Event, Material, MaterialRequest, RequestSignature, Project,OrganizationUnit, RequestSignature, Service, ServiceRequest, WareHouse, WareHouseSheetLine

admin.site.register(EmployeeDocument)
# admin.site.register(Request)
admin.site.register(RequestSignature)
# admin.site.register(DeviceConfiguration)
admin.site.register(Project)
admin.site.register(OrganizationUnit)
admin.site.register(EmployeeSpeciality)
admin.site.register(Employee)
admin.site.register(Material)
admin.site.register(WareHouse)
admin.site.register(Event)
admin.site.register(MaterialRequest)
admin.site.register(ServiceRequest)
admin.site.register(Service)
admin.site.register(WareHouseMaterial)
admin.site.register(WareHouseExportSheet)
admin.site.register(WareHouseImportSheet)
admin.site.register(WareHouseSheetLine)
admin.site.register(Employer)