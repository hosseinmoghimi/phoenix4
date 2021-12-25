from django.urls import path
from . import views,apis
from .apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('property_media/<int:pk>/',views.PropertyViews().property_media,name='property_media'),
    path('property/<int:property_id>/',views.PropertyViews().property,name='property'),
    path('car/<int:pk>/',views.CarViews().car,name='car'),
    path('agent/<int:pk>/',views.BasicViews().agent,name='agent'),

    path('add_location/',apis.PropertyApi().add_location,name="add_location"),
    path('add_property_image/',apis.PropertyApi().add_property_image,name="add_property_image"),
    path('add_feature/',apis.PropertyApi().add_feature,name="add_feature"),
]
