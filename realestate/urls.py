from django.urls import path
from . import views,apis
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('property_media/<int:pk>/',views.PropertyViews().property_media,name='property_media'),
    path('property/<int:pk>/',views.PropertyViews().property,name='property'),

    path('add_location/',apis.PropertyApi().add_location,name="add_location"),
]
