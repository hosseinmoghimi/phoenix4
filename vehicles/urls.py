from django.urls import path
from .apps import APP_NAME
from . import views,apis
app_name=APP_NAME
from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path("",login_required(views.BasicViews().home),name="home"),
    path("driver/<int:driver_id>/",login_required(views.DriverViews().driver),name="driver"),
    path("vehicle/<int:vehicle_id>/",login_required(views.VehicleViews().vehicle),name="vehicle"),
    path("vehicle_work_event/<int:pk>/",login_required(views.VehicleWorkEventViews().vehicle_work_event),name="vehicleworkevent"),
    path("area/<int:area_id>/",login_required(views.AreaViews().area),name="area"),
    path("vehicleevent/<int:pk>/",login_required(views.AreaViews().area),name="vehicleevent"),
    path("maintenance/<int:maintenance_id>/",login_required(views.MaintenanceViews().maintenance),name="maintenance"),
    path("service_man/<int:service_man_id>/",login_required(views.ServiceManViews().service_man),name="service_man"),
    path("work_shift/<int:pk>/",login_required(views.WorkShiftViews().work_shift),name="workshift"),
    path("trip/<int:trip_id>/",login_required(views.TripViews().trip),name="trip"),
    path("trips/<int:category_id>/<int:vehicle_id>/<int:driver_id>/<int:trip_path_id>/",login_required(views.TripViews().trips),name="trips"),
    path("passenger/<int:passenger_id>/",login_required(views.PassengerViews().passenger),name="passenger"),
    path("trip_path/<int:trip_path_id>/",login_required(views.TripViews().trip_path),name='trippath'),

    path("add_passenger_to_trip/",login_required(apis.TripApi().add_passenger_to_trip),name='add_passenger_to_trip'),
    path("add_work_shift/",login_required(apis.WorkShiftApi().add_work_shift),name='add_work_shift'),
    path("add_vehicle_work_event/",login_required(apis.VehicleWorkEventApi().add_vehicle_work_event),name='add_vehicle_work_event'),
    path("add_new_trip/",login_required(apis.TripApi().add_new_trip),name='add_new_trip'),
    path("add_maintenance/",login_required(apis.MaintenanceApi().add_maintenance),name='add_maintenance'),
    path("add_new_vehicle/",login_required(apis.VehicleApi().add_new_vehicle),name='add_new_vehicle'),
]
