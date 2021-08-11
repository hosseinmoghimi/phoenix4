from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('search/',views.BasicViews().search,name="search"),
    path('project/<int:pk>/',views.ProjectViews().project,name="project"),
    path('project-materials-order/<int:pk>/',views.ProjectViews().project_materials_order,name="project_materials_order"),
    path('project-services-order/<int:pk>/',views.ProjectViews().project_services_order,name="project_services_order"),
    path('projects-chart/<int:pk>/',views.ProjectViews().projects_chart,name="projects_chart"),
    path('employer/<int:pk>/',views.OrganizationUnitViews().employer,name="employer"),
    path('employee/<int:pk>/',views.EmployeeViews().employee,name="employee"),
    path('organizationunit/<int:pk>/',views.OrganizationUnitViews().organization_unit,name="organizationunit"),
    path('material/<int:pk>/',views.MaterialViews().material,name="material"),
    path('materialrequest/<int:pk>/',views.MaterialViews().material_request,name="materialrequest"),
    path('service/<int:pk>/',views.ServiceViews().service,name="service"),
    
    path('materials/',views.MaterialViews().materials,name="materials"),
    path('services/',views.ServiceViews().services,name="services"),
    path('servicerequest/<int:pk>/',views.ServiceViews().service_request,name="servicerequest"),
    path('event/<int:pk>/',views.EventViews().event,name="event"),
    path('location/<int:pk>/',views.LoactionViews().location,name="location"),
    
    
    path('add_event/',apis.EventApi().add_event,name="add_event"),
    path('add_signature/',apis.ProjectApi().add_signature,name="add_signature"),
    path('edit_project/',apis.ProjectApi().edit_project,name="edit_project"),
    path('add_employer/',apis.OrganizationUnitApi().add_employer,name="add_employer"),
    path('add_employee/',apis.OrganizationUnitApi().add_employee,name="add_employee"),
    path('add_service_request/',apis.ServiceApi().add_service_request,name="add_service_request"),
    path('add_service/',apis.ServiceApi().add_service,name="add_service"),
    path('add_material_request/',apis.MaterialApi().add_material_request,name="add_material_request"),
    path('add_material/',apis.MaterialApi().add_material,name="add_material"),
    path('add_organization_unit/',apis.OrganizationUnitApi().add_organization_unit,name="add_organization_unit"),
    path('add_project/',apis.ProjectApi().add_project,name="add_project"),
    path('add_location/',apis.LocationApi().add_location,name="add_location"),
    path('add_existing_location/',apis.LocationApi().add_existing_location,name="add_existing_location"),
    
    path('add_material/',apis.MaterialApi().add_material,name="add_material"),
]


