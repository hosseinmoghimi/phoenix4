from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('location/<int:pk>/',views.LocationViews().location,name='location'),
    path('locations/',views.LocationViews().locations,name='locations'),
    path('add_location/',apis.LocationApi().add_location,name='add_location'),
]
