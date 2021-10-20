from django.contrib import admin

from vehicles.models import Area, Driver, Maintenance, Passenger, ServiceMan, Trip, TripPath, Vehicle, VehicleEvent, VehicleLocation, VehicleWorkEvent, WorkShift

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Passenger)
admin.site.register(Driver)
admin.site.register(TripPath)
admin.site.register(Area)
admin.site.register(VehicleLocation)
admin.site.register(VehicleEvent)
admin.site.register(WorkShift)
admin.site.register(ServiceMan)
admin.site.register(VehicleWorkEvent)
admin.site.register(Maintenance)
admin.site.register(Trip)
