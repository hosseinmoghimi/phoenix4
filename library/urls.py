from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    path('book/<int:pk>/',login_required(views.BookViews().book),name="book"),
    path('add_book/',login_required(apis.BookApi().add_book),name="add_book"),
]


