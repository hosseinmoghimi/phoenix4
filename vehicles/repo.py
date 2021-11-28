from django.http import request
from authentication.repo import ProfileRepo
from core import repo as CoreRepo
from vehicles.enums import VehicleColorEnum, VehicleTypeEnum
from vehicles.serializers import VehicleWorkEventSerializer
from .models import Passenger, Trip, TripPath, Vehicle, VehicleWorkEvent, Driver, Maintenance, WorkShift, Area, ServiceMan
from .apps import APP_NAME
from django.utils import timezone, translation
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
        vehicle.title=kwargs['title'] if 'title' in kwargs else None
        vehicle.vehicle_type =kwargs['vehicle_type'] if 'vehicle_type' in kwargs else VehicleTypeEnum.SEDAN
        vehicle.color =kwargs['color'] if 'color' in kwargs else VehicleColorEnum.SEFID
        vehicle.year =kwargs['year'] if 'year' in kwargs else 2015
        vehicle.kilometer =kwargs['kilometer'] if 'kilometer' in kwargs else 0
        
        vehicle.save()
        return vehicle


class PassengerRepo():

    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Passenger.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me = Passenger.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects=self.objects
        if 'passenger_id' in kwargs:
            objects=objects.filter(passenger_id=kwargs['passenger_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(driver_id=kwargs['driver_id'])
        if 'destination_id' in kwargs:
            objects=objects.filter(destination_id=kwargs['destination_id'])
        if 'source_id' in kwargs:
            objects=objects.filter(source_id=kwargs['source_id'])
        return objects.all()

    def passenger(self, *args, **kwargs):
        pk=0
        if 'passenger_id' in kwargs:
            pk = kwargs['passenger_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class TripRepo():

    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects=Trip.objects.filter(pk=0)
        self.profile = ProfileRepo(user=self.user).me
        self.driver = DriverRepo(user=self.user).me
        self.passenger = PassengerRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+".view_trip"):
            self.objects = Trip.objects
        elif self.driver is not None:
            self.objects=Trip.objects.filter(driver_id=self.driver.id)
        elif self.passenger is not None:
            self.objects=self.passenger.trip_set.all()

    def list(self, *args, **kwargs):
        objects=self.objects
        if 'passenger_id' in kwargs and kwargs['passenger_id']>0:
            passenger_id=kwargs['passenger_id']
            trips_ids=[]
            passenger=PassengerRepo(request=self.request).passenger(pk=passenger_id)
            for trip in self.objects.all():
                if passenger in trip.passengers.all():
                    trips_ids.append(trip.id)
            return self.objects.filter(id__in=trips_ids)
        if 'trip_path_id' in kwargs and kwargs['trip_path_id']>0:
            trip_path_id=kwargs['trip_path_id']
            trips_ids=[]
            trip_path=TripPathRepo(request=self.request).trip_path(pk=trip_path_id)
            for trip in self.objects.all():
                if trip_path in trip.paths.all():
                    trips_ids.append(trip.id)
            return self.objects.filter(id__in=trips_ids)

        if 'vehicle_id' in kwargs and kwargs['vehicle_id']>0:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'category_id' in kwargs and kwargs['category_id']>0:
            objects=objects.filter(category_id=kwargs['category_id'])
        if 'driver_id' in kwargs and kwargs['driver_id']>0:
            objects=objects.filter(driver_id=kwargs['driver_id'])
        # if 'destination_id' in kwargs:
        #     objects=objects.filter(destination_id=kwargs['destination_id'])
        # if 'source_id' in kwargs:
        #     objects=objects.filter(source_id=kwargs['source_id'])
        return objects.all()

    def trip(self, *args, **kwargs):
        pk=0
        if 'trip_id' in kwargs:
            pk = kwargs['trip_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_passenger_to_trip(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_passenger"):
            return
        trip=TripRepo(request=self.request).trip(*args, **kwargs)
        passenger=PassengerRepo(request=self.request).passenger(*args, **kwargs)
        if trip is not None and passenger is not None:
            trip.passengers.add(passenger)
        return passenger

    def add_trip(self,*args, **kwargs):
        me_passenger=PassengerRepo(request=self.request).me
        passengers =kwargs['passengers'] if 'passengers' in kwargs else []
        if self.user.has_perm(APP_NAME+".add_trip"):
            pass
        elif me_passenger is not None and passengers==[me_passenger.id]:
            pass
        else:
            return
        trip=Trip()
        trip.title=kwargs['title'] if 'title' in kwargs else None
        trip.vehicle_id=kwargs['vehicle_id'] if 'vehicle_id' in kwargs else None
        # trip.source_id =kwargs['source_id'] if 'source_id' in kwargs else None
        # trip.destination_id =kwargs['destination_id'] if 'destination_id' in kwargs else None
        trip.driver_id =kwargs['driver_id'] if 'driver_id' in kwargs else None
        trip.cost =kwargs['cost'] if 'cost' in kwargs else 10000
        trip.distance =kwargs['distance'] if 'distance' in kwargs else 5
        trip.delay =kwargs['delay'] if 'delay' in kwargs else 0
        trip.save()
        passenger_repo=PassengerRepo(request=self.request)
        for passenger_id in passengers:
            passenger=passenger_repo.passenger(pk=passenger_id)
            trip.passengers.add(passenger)
        paths =kwargs['paths'] if 'paths' in kwargs else []
        for path in paths:
            path1=TripPathRepo(request=self.request).trip_path(pk=path['id'])
            trip.paths.add(path1)
        trip.date_tripped =kwargs['date_tripped'] if 'date_tripped' in kwargs else timezone.now()
        
        trip.save()
        return trip
   

class TripPathRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = TripPath.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects=self.objects
        if 'passenger_id' in kwargs:
            passenger_id=kwargs['passenger_id']
            trips_ids=[]
            passenger=PassengerRepo(request=self.request).passenger(pk=passenger_id)
            for trip in self.objects.all():
                if passenger in trip.passengers.all():
                    trips_ids.append(trip.id)
            return self.objects.filter(id__in=trips_ids)
            
        if 'vehicle_id' in kwargs:
            objects=objects.filter(vehicle_id=kwargs['vehicle_id'])
        if 'driver_id' in kwargs:
            objects=objects.filter(driver_id=kwargs['driver_id'])
        if 'destination_id' in kwargs:
            objects=objects.filter(destination_id=kwargs['destination_id'])
        if 'source_id' in kwargs:
            objects=objects.filter(source_id=kwargs['source_id'])
        return objects.all()

    def trip_path(self, *args, **kwargs):
        
        if 'source_id' in kwargs and 'destination_id' in kwargs:
            source_id = kwargs['source_id']
            destination_id = kwargs['destination_id']
            return self.objects.filter(source_id=source_id).filter(destination_id=destination_id).first()
        if 'trip_path_id' in kwargs:
            pk = kwargs['trip_path_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_trip_path(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_trippath"):
            return
        source_id=kwargs['source_id'] if 'source_id' in kwargs else 0
        destination_id=kwargs['destination_id'] if 'destination_id' in kwargs else 0
        duration=kwargs['duration'] if 'duration' in kwargs else 0
        distance=kwargs['distance'] if 'distance' in kwargs else 0
        cost=kwargs['cost'] if 'cost' in kwargs else 0
        trip_path=self.trip_path(source_id=source_id,destination_id=destination_id)
        if trip_path is None:
            trip_path=TripPath()
            trip_path.source_id=source_id
            trip_path.destination_id=destination_id
        trip_path.duration=duration
        trip_path.distance=distance
        trip_path.cost=cost
        trip_path.save()
        return trip_path


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
        self.profile = ProfileRepo(user=self.user).me
        self.me = Driver.objects.filter(profile=self.profile).first()

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


    def add_driver(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_driver"):
            return
        driver=Driver()
        driver.profile_id=kwargs['profile_id'] if 'profile_id' in kwargs else 0
        driver.start_date=kwargs['start_date'] if 'start_date' in kwargs else timezone.now()
        driver.end_date=kwargs['end_date'] if 'end_date' in kwargs else timezone.now()
        driver.save()
        return driver


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
