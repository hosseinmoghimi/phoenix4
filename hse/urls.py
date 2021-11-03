from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('blog/<int:pk>/',login_required(views.BlogViews().blog),name="blog"),
   
    path('add_blog/',login_required(apis.BlogApi().add_blog),name="add_blog"),
]


