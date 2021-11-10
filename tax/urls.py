from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('tax/<int:pk>/',login_required(views.TaxViews().tax),name="tax"),
   
    path('add_tax/',login_required(apis.TaxApi().add_tax),name="add_tax"),
]


