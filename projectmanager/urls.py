from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('search/',login_required(views.BasicViews().search),name="search"),
    path('projects/',login_required(views.ProjectViews().projects),name="projects"),
    path('events/',login_required(views.EventViews().events),name="events"),
    path('material_requests/',login_required(views.MaterialRequestViews().material_requests),name="material_requests"),
    path('service_requests/',login_required(views.ServiceRequestViews().service_requests),name="service_requests"),
    path('project/<int:pk>/',login_required(views.ProjectViews().project),name="project"),
    path('sampleform/<int:pk>/',login_required(views.SampleFormViews().sampleform),name="sampleform"),
    
    path('dashboard/<int:employee_id>/',login_required(views.EmployeeViews().dashboard),name="dashboard"),
    path('guantt/<int:project_id>/',login_required(views.ProjectViews().guantt),name="guantt"),
    path('project_events_chart/<int:project_id>/',login_required(views.EventViews().project_events_chart),name="project_events_chart"),
    path('project_events_chart2/<int:project_id>/',login_required(views.EventViews().project_events_chart2),name="project_events_chart2"),
    path('project_events_chart3/<int:project_id>/',login_required(views.EventViews().project_events_chart3),name="project_events_chart3"),
    
    path('project-materials-order/<int:pk>/<int:tax_percent>/<unit>/',login_required(views.ProjectViews().project_materials_order),name="project_materials_order"),
    path('project-services-order/<int:pk>/<int:tax_percent>/<unit>/',login_required(views.ProjectViews().project_services_order),name="project_services_order"),
    
    path('projects-chart/<int:pk>/',login_required(views.ProjectViews().projects_chart),name="projects_chart"),
    path('organization_units_chart/<int:employer_id>/',login_required(views.OrganizationUnitViews().organization_units_chart),name="organization_units_chart"),
    path('employer/<int:pk>/',login_required(views.OrganizationUnitViews().employer),name="employer"),
    path('employee/<int:pk>/',login_required(views.EmployeeViews().employee),name="employee"),
    path('employees/<int:employer_id>/<int:organization_unit_id>/',login_required(views.EmployeeViews().employees),name="employees"),
    path('organizationunit/<int:pk>/',login_required(views.OrganizationUnitViews().organization_unit),name="organizationunit"),
    path('material/<int:pk>/',login_required(views.MaterialViews().material),name="material"),
    path('materialrequest/<int:pk>/',login_required(views.MaterialRequestViews().material_request),name="materialrequest"),
    path('service/<int:pk>/',login_required(views.ServiceViews().service),name="service"),
    path('ware_house_sheet_line/<int:pk>/',login_required(views.WareHouseSheetViews().ware_house_sheet_line),name="warehousesheetline"),
    path('ware_house_sheet/<int:pk>/',login_required(views.WareHouseSheetViews().ware_house_sheet),name="ware_house_sheet"),
    path('ware_house/<int:pk>/',login_required(views.WareHouseViews().ware_house),name="warehouse"),
    path('ware_house_import_sheet/<int:pk>/',login_required(views.WareHouseSheetViews().ware_house_import_sheet),name="warehouseimportsheet"),
    path('ware_house_export_sheet/<int:pk>/',login_required(views.WareHouseSheetViews().ware_house_export_sheet),name="warehouseexportsheet"),
    path('copy_project_request/<int:destination_project_id>/',login_required(views.ProjectViews().copy_project_request),name="copy_project_request"),
    
    path('materials/',login_required(views.MaterialViews().materials),name="materials"),
    path('services/',login_required(views.ServiceViews().services),name="services"),
    path('servicerequest/<int:pk>/',login_required(views.ServiceRequestViews().service_request),name="servicerequest"),
    path('event/<int:pk>/',login_required(views.EventViews().event),name="event"),
    path('add_signature/',login_required(views.RequestViews().add_signature),name="add_signature"),
    
    
    path('add_event/',login_required(apis.EventApi().add_event),name="add_event"),
    path('add_signature/',login_required(apis.ProjectApi().add_signature),name="add_signature"),
    path('api/add_signature/',login_required(apis.ProjectApi().add_signature),name="api_add_signature"),
    path('edit_project/',login_required(apis.ProjectApi().edit_project),name="edit_project"),
    path('add_employer/',login_required(apis.OrganizationUnitApi().add_employer),name="add_employer"),
    path('add_employee/',login_required(apis.EmployeeApi().add_employee),name="add_employee"),
    path('add_service_request/',login_required(apis.ServiceRequestApi().add_service_request),name="add_service_request"),
    path('add_service/',login_required(apis.ServiceApi().add_service),name="add_service"),
    path('add_material_request/',login_required(apis.MaterialRequestApi().add_material_request),name="add_material_request"),
    path('add_material/',login_required(apis.MaterialApi().add_material),name="add_material"),
    path('add_organization_unit/',login_required(apis.OrganizationUnitApi().add_organization_unit),name="add_organization_unit"),
    path('add_project/',login_required(apis.ProjectApi().add_project),name="add_project"),
    path('add_existing_location/',login_required(apis.ProjectApi().add_location),name="add_location"),
    path('add_material_request_to_ware_house_sheet/',login_required(apis.WareHouseSheetApi().add_material_request_to_ware_house_sheet),name="add_material_request_to_ware_house_sheet"),
    
    path('add_material/',login_required(apis.MaterialApi().add_material),name="add_material"),
]


