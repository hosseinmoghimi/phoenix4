from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path("",login_required(views.BasicViews().home),name="home"),
    
    path("trip_request/",login_required(views.TripViews().trip_request),name="trip_request"),



    path("areas/",login_required(views.AreaViews().areas),name="areas"),
    path("area/<int:area_id>/",login_required(views.AreaViews().area),name="area"),

    path("drivers/",login_required(views.DriverViews().drivers),name="drivers"),
    path("driver/<int:driver_id>/",login_required(views.DriverViews().driver),name="driver"),
    
    path("vehicles/",login_required(views.VehicleViews().vehicles),name="vehicles"),
    path("vehicle/<int:vehicle_id>/",login_required(views.VehicleViews().vehicle),name="vehicle"),
    
    path("trips/<int:category_id>/<int:vehicle_id>/<int:driver_id>/<int:trip_path_id>/<int:passenger_id>/",login_required(views.TripViews().trips),name="trips"),
    path("trip/<int:trip_id>/",login_required(views.TripViews().trip),name="trip"),

    path("trip_paths/",login_required(views.TripViews().trip_paths),name='trippaths'),
    path("trip_path/<int:trip_path_id>/",login_required(views.TripViews().trip_path),name='trippath'),
    
    path("vehicle_work_event/<int:pk>/",login_required(views.VehicleWorkEventViews().vehicle_work_event),name="vehicleworkevent"),
    path("vehicleevent/<int:pk>/",login_required(views.AreaViews().area),name="vehicleevent"),
    path("maintenance/<int:maintenance_id>/",login_required(views.MaintenanceViews().maintenance),name="maintenance"),
    path("service_mans/",login_required(views.ServiceManViews().service_mans),name="service_mans"),
    path("service_man/<int:service_man_id>/",login_required(views.ServiceManViews().service_man),name="service_man"),
    path("work_shift/<int:pk>/",login_required(views.WorkShiftViews().work_shift),name="workshift"),
    path("passengers/",login_required(views.PassengerViews().passengers),name="passengers"),
    path("passenger/<int:passenger_id>/",login_required(views.PassengerViews().passenger),name="passenger"),


    path("add_passenger/",login_required(apis.PassengerApi().add_new_passenger),name='add_passenger'),
    path("add_passenger_to_trip/",login_required(apis.TripApi().add_passenger_to_trip),name='add_passenger_to_trip'),
    path("add_work_shift/",login_required(apis.WorkShiftApi().add_work_shift),name='add_work_shift'),
    path("add_trip_path/",login_required(apis.TripApi().add_trip_path),name='add_trip_path'),
    path("add_vehicle_work_event/",login_required(apis.VehicleWorkEventApi().add_vehicle_work_event),name='add_vehicle_work_event'),
    path("add_new_trip/",login_required(apis.TripApi().add_new_trip),name='add_new_trip'),
    path("add_new_driver/",login_required(apis.DriverApi().add_new_driver),name='add_new_driver'),
    path("add_maintenance/",login_required(apis.MaintenanceApi().add_maintenance),name='add_maintenance'),
    path("add_new_vehicle/",login_required(apis.VehicleApi().add_new_vehicle),name='add_new_vehicle'),
    path("filter_trip/",login_required(apis.TripApi().filter_trip),name='filter_trip'),
]
