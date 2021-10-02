from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    
    path("",views.BasicViews().home,name="home"),
    path("driver/<int:pk>/",views.VehicleViews().vehicle,name="driver"),
    path("vehicle/<int:vehicle_id>/",views.VehicleViews().vehicle,name="vehicle"),
    path("vehicle_work_event/<int:pk>/",views.VehicleViews().vehicle,name="vehicle_work_event"),


    path("add_work_shift/",apis.WorkShiftApi().add_work_shift,name='add_work_shift'),
]
