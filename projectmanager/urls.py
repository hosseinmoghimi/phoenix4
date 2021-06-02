from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('search/',views.BasicViews().search,name="search"),
    path('employer/<int:pk>/',views.OrganizationUnitViews().employer,name="employer"),
    path('project/<int:pk>/',views.ProjectViews().project,name="project"),
    path('material/<int:pk>/',views.MaterialViews().material,name="material"),
    path('employee/<int:pk>/',views.EmployeeViews().employee,name="employee"),
    path('organizationunit/<int:pk>/',views.OrganizationUnitViews().organization_unit,name="organizationunit"),
    path('materialrequest/<int:pk>/',views.MaterialViews().material_request,name="materialrequest"),
    
    
    path('add_employer/',apis.OrganizationUnitApi().add_employer,name="add_employer"),
    path('add_material_request/',apis.MaterialApi().add_material_request,name="add_material_request"),
    path('add_material/',apis.MaterialApi().add_material,name="add_material"),
    path('add_organization_unit/',apis.OrganizationUnitApi().add_organization_unit,name="add_organization_unit"),
    path('add_project/',apis.ProjectApi().add_project,name="add_project"),
    path('add_material/',apis.MaterialApi().add_material,name="add_material"),
]


