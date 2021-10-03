from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
urlpatterns = [
    
    path("",views.BasicViews().home,name="home"),
    path("driver/<int:driver_id>/",views.DriverViews().driver,name="driver"),
    path("vehicle/<int:vehicle_id>/",views.VehicleViews().vehicle,name="vehicle"),
    path("vehicle_work_event/<int:pk>/",views.VehicleViews().vehicle,name="vehicle_work_event"),
    path("area/<int:area_id>/",views.AreaViews().area,name="area"),
    path("vehicleevent/<int:pk>/",views.AreaViews().area,name="vehicleevent"),
    path("maintenance/<int:maintenance_id>/",views.MaintenanceViews().maintenance,name="maintenance"),
    path("service_man/<int:service_man_id>/",views.ServiceManViews().service_man,name="service_man"),


    path("add_work_shift/",apis.WorkShiftApi().add_work_shift,name='add_work_shift'),
    path("add_maintenance/",apis.MaintenanceApi().add_maintenance,name='add_maintenance'),
]
