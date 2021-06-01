from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('project/<int:pk>/',views.ProjectViews().project,name="project"),
    path('material/<int:pk>/',views.MaterialViews().material,name="material"),
    path('employee/<int:pk>/',views.EmployeeViews().employee,name="employee"),
    path('organizationunit/<int:pk>/',views.OrganizationUnitViews().organization_unit,name="organizationunit"),
    
    
    path('add_organization_unit/',apis.OrganizationUnitApi().add_organization_unit,name="add_organization_unit"),
    path('add_project/',apis.ProjectApi().add_project,name="add_project"),
    path('add_material/',apis.MaterialApi().add_material,name="add_material"),
]


