from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path("",login_required(views.BasicViews().home),name="home"),
    path("driver/<int:driver_id>/",views.DriverViews().driver,name="driver"),
    path("vehicle/<int:vehicle_id>/",views.VehicleViews().vehicle,name="vehicle"),
    path("vehicle_work_event/<int:pk>/",views.VehicleWorkEventViews().vehicle_work_event,name="vehicleworkevent"),
    path("area/<int:area_id>/",views.AreaViews().area,name="area"),
    path("vehicleevent/<int:pk>/",views.AreaViews().area,name="vehicleevent"),
    path("maintenance/<int:maintenance_id>/",views.MaintenanceViews().maintenance,name="maintenance"),
    path("service_man/<int:service_man_id>/",views.ServiceManViews().service_man,name="service_man"),
    path("work_shift/<int:pk>/",views.WorkShiftViews().work_shift,name="workshift"),
    path("trip/<int:trip_id>/",views.TripViews().trip,name="trip"),
    path("trips/",views.TripViews().trips,name="trips"),
    path("passenger/<int:passenger_id>/",views.PassengerViews().passenger,name="passenger"),
    path("trip_path/<int:trip_path_id>/",views.TripViews().trip_path,name='trippath'),


    path("add_work_shift/",apis.WorkShiftApi().add_work_shift,name='add_work_shift'),
    path("add_vehicle_work_event/",apis.VehicleWorkEventApi().add_vehicle_work_event,name='add_vehicle_work_event'),
    path("add_new_trip/",apis.TripApi().add_new_trip,name='add_new_trip'),
    path("add_maintenance/",apis.MaintenanceApi().add_maintenance,name='add_maintenance'),
    path("add_new_vehicle/",apis.VehicleApi().add_new_vehicle,name='add_new_vehicle'),
]
