from django.urls import path
from .apps import APP_NAME
from . import views
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name='home'),
]
