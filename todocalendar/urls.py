from .apps import APP_NAME
from . import views,apis
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path('',views.BasicViews().home,name='home'),
    path('appointment/<int:appointment_id>/',views.AppointmentViews().appointment,name='appointment'),
    path('add_person/',apis.AppointmentApi().add_person,name='add_person'),
]
