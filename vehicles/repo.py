from django.http import request
from authentication.repo import ProfileRepo
from core import repo as CoreRepo
from vehicles.enums import VehicleColorEnum, VehicleTypeEnum
from vehicles.serializers import VehicleWorkEventSerializer
from .models import Trip, Vehicle, VehicleWorkEvent, Driver, Maintenance, WorkShift, Area, ServiceMan
from .apps import APP_NAME
from django.utils import timezone
now=timezone.now()

class VehicleRepo():

    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Vehicle.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        return self.objects.all()

    def vehicle(self, *args, **kwargs):
        if 'vehicle_id' in kwargs:
            pk = kwargs['vehicle_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_vehicle(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_vehicle"):
            return
        vehicle=Vehicle()
        vehicle.name=kwargs['name'] if 'name' in kwargs else None
        vehicle.vehicle_type =kwargs['vehicle_type'] if 'vehicle_type' in kwargs else VehicleTypeEnum.SEDAN
        vehicle.color =kwargs['color'] if 'color' in kwargs else VehicleColorEnum.SEFID
        vehicle.year =kwargs['year'] if 'year' in kwargs else 2015
        vehicle.kilometer =kwargs['kilometer'] if 'kilometer' in kwargs else 0
        
        vehicle.save()
        return vehicle

class TripRepo():

    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Trip.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects=self.objects
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(driver_id=kwargs['driver_id'])
        if 'destination_id' in kwargs:
            objects=objects.filter(destination_id=kwargs['destination_id'])
        if 'source_id' in kwargs:
            objects=objects.filter(source_id=kwargs['source_id'])
        return objects.all()

    def trip(self, *args, **kwargs):
        if 'trip_id' in kwargs:
            pk = kwargs['trip_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_trip(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_trip"):
            return
        trip=Trip()
        trip.title=kwargs['title'] if 'title' in kwargs else None
        trip.vehicle_id=kwargs['vehicle_id'] if 'vehicle_id' in kwargs else None
        trip.source_id =kwargs['source_id'] if 'source_id' in kwargs else None
        trip.destination_id =kwargs['destination_id'] if 'destination_id' in kwargs else None
        trip.driver_id =kwargs['driver_id'] if 'driver_id' in kwargs else None
        trip.cost =kwargs['cost'] if 'cost' in kwargs else 10000
        trip.distance =kwargs['distance'] if 'distance' in kwargs else 5
        trip.date_tripped =kwargs['date_tripped'] if 'date_tripped' in kwargs else timezone.now()
        
        trip.save()
        return trip

class ServiceManRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ServiceMan.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        return self.objects.all()

    def service_man(self, *args, **kwargs):
        if 'service_man_id' in kwargs:
            pk = kwargs['service_man_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class AreaRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Area.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        return self.objects.all()

    def area(self, *args, **kwargs):
        if 'area_id' in kwargs:
            pk = kwargs['area_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class DriverRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Driver.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        return self.objects.all()

    def driver(self, *args, **kwargs):
        if 'driver_id' in kwargs:
            pk = kwargs['driver_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class MaintenanceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Maintenance.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects= self.objects.all()
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'maintenance_type' in kwargs:
            objects=objects.filter(maintenance_type=kwargs['maintenance_type'])
        if 'service_man_id' in kwargs:
            objects=objects.filter(service_man_id=kwargs['service_man_id'])
        if 'maintenance_type' in kwargs:
            objects=objects.filter(maintenance_type=kwargs['maintenance_type'])
        return objects

    def maintenance(self, *args, **kwargs):
        pk=0
        if 'maintenance_id' in kwargs:
            pk = kwargs['maintenance_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_maintenance(self, *args, **kwargs):
        
        if not self.user.has_perm(APP_NAME+".add_manitenance"):
            return
        paid=kwargs['paid'] if 'paid' in kwargs else 0
        service_man_id=kwargs['service_man_id'] if 'service_man_id' in kwargs else 0
        maintenance_type=kwargs['maintenance_type'] if 'maintenance_type' in kwargs else ""
        description=kwargs['description'] if 'description' in kwargs else ""
        title=kwargs['title'] if 'title' in kwargs else ""
        vehicle_id=kwargs['vehicle_id'] if 'vehicle_id' in kwargs else 0
        event_datetime=kwargs['event_datetime'] if 'event_datetime' in kwargs else ""
        kilometer=kwargs['kilometer'] if 'kilometer' in kwargs else 0

        maintenance = Maintenance()
        maintenance.vehicle_id=vehicle_id
        maintenance.title=title
        maintenance.description=description
        maintenance.maintenance_type=maintenance_type
        maintenance.service_man_id=service_man_id
        maintenance.event_datetime=event_datetime
        maintenance.paid=paid
        maintenance.kilometer=kilometer
        maintenance.save()
        return maintenance

    def get_report(self, *args, **kwargs):
        objects = self.objects.all()
        if 'service_man_id' in kwargs:
            service_man_id = kwargs['service_man_id']
            if service_man_id is not None and service_man_id > 0:
                objects = objects.filter(service_man_id=service_man_id)
        if 'start_date' in kwargs:
            start_date = kwargs['start_date']
            if start_date is not None and not start_date == "":
                objects = objects.filter(event_time__gte=start_date)
        if 'end_date' in kwargs:
            end_date = kwargs['end_date']
            if end_date is not None and not end_date == "":
                objects = objects.filter(event_time__lte=end_date)
        if 'vehicle_id' in kwargs:
            vehicle_id = kwargs['vehicle_id']
            if not vehicle_id == 0:
                objects = objects.filter(vehicle_id=vehicle_id)
        if 'maintenance_type' in kwargs:
            maintenance_type = kwargs['maintenance_type']
            if maintenance_type is not None and not maintenance_type == "":
                objects = objects.filter(maintenance_type=maintenance_type)
        return objects


class WorkShiftRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = WorkShift.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'vehicle_id' in kwargs:
            objects = objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'area_id' in kwargs:
            objects = objects.filter(area_id=kwargs['area_id'])
        if 'driver_id' in kwargs:
            objects = objects.filter(driver_id=kwargs['driver_id'])
        if 'vehicle_work_event_id' in kwargs:
            vehicle_work_event_id=kwargs['vehicle_work_event_id']
            vehicle_work_event=VehicleWorkEvent.objects.filter(pk=vehicle_work_event_id).first()
            if vehicle_work_event is None:
                return []
            
            objects = vehicle_work_event.workshift_set.all()
        return objects

    def work_shift(self, *args, **kwargs):
        if 'work_shift_id' in kwargs:
            pk = kwargs['work_shift_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_work_shift(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_workshift"):
            return
        area_id=kwargs['area_id'] if 'area_id' in kwargs else 0
        vehicle_id=kwargs['vehicle_id'] if 'vehicle_id' in kwargs else 0
        start_datetime=kwargs['start_datetime'] if 'start_datetime' in kwargs else now
        end_datetime=kwargs['end_datetime'] if 'end_datetime' in kwargs else now
        driver_id=kwargs['driver_id'] if 'driver_id' in kwargs else 0
        income=kwargs['income'] if 'income' in kwargs else 0
        outcome=kwargs['outcome'] if 'outcome' in kwargs else 0
        description=kwargs['description'] if 'description' in kwargs else ""

        work_shift=WorkShift()
        work_shift.area_id=area_id
        work_shift.vehicle_id=vehicle_id
        work_shift.start_time=start_datetime
        work_shift.end_time=end_datetime
        work_shift.driver_id=driver_id
        work_shift.income=income
        work_shift.outcome=outcome
        work_shift.description=description
        work_shift.save()
        return work_shift


class VehicleWorkEventRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = VehicleWorkEvent.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'vehicle_id' in kwargs:
            objects = objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'work_shift_id' in kwargs:
            objects = objects.filter(work_shift_id=kwargs['work_shift_id'])
        return objects

    def vehicle_work_event(self, *args, **kwargs):
        if 'vehicle_work_event_id' in kwargs:
            pk = kwargs['vehicle_work_event_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def get_report(self, *args, **kwargs):
        objects = self.objects.all()
        if 'start_date' in kwargs:
            start_date = kwargs['start_date']
            if start_date is not None and not start_date == "":
                objects = objects.filter(event_time__gte=start_date)
        if 'end_date' in kwargs:
            end_date = kwargs['end_date']
            if end_date is not None and not end_date == "":
                objects = objects.filter(event_time__lte=end_date)
        if 'vehicle_id' in kwargs:
            vehicle_id = kwargs['vehicle_id']
            if not vehicle_id == 0:
                objects = objects.filter(vehicle_id=vehicle_id)
        if 'event_type' in kwargs:
            event_type = kwargs['event_type']
            if event_type is not None and not event_type == "":
                objects = objects.filter(event_type=event_type)
        return objects


    def add_vehicle_work_event(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_vehicleworkevent"):
            return
        work_shift_id=kwargs["work_shift_id"] if "work_shift_id" in kwargs else 0
        event_type=kwargs["event_type"] if "event_type" in kwargs else ""
        vehicle_id=kwargs["vehicle_id"] if "vehicle_id" in kwargs else 0
        event_datetime=kwargs["event_datetime"] if "event_datetime" in kwargs else timezone.now()
        description=kwargs["description"] if "description" in kwargs else ""
        kilometer=kwargs["kilometer"] if "kilometer" in kwargs else 0
        work_shift=WorkShiftRepo(request=self.request).work_shift(pk=work_shift_id)
        vehicle_work_event=VehicleWorkEvent()
        vehicle_work_event.work_shift_id=work_shift_id
        vehicle_work_event.event_type=event_type
        vehicle_work_event.vehicle_id=work_shift.vehicle_id
        vehicle_work_event.event_datetime=event_datetime
        vehicle_work_event.description=description
        vehicle_work_event.kilometer=kilometer
        vehicle_work_event.save()
        return vehicle_work_event
