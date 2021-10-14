from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('location/<int:pk>/',views.BasicViews().location,name='location'),
]
