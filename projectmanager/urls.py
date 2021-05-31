from django.shortcuts import render
from .apps import APP_NAME
from . import views
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name="home"),
    path('project/<int:pk>/',views.ProjectViews().project,name="project"),
]


