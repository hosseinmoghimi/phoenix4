from authentication.repo import ProfileRepo
from core import repo as CoreRepo
from .models import Vehicle, VehicleWorkEvent, Driver, Maintenance, WorkShift, Area, ServiceMan
from .apps import APP_NAME


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
        return self.objects.all()

    def maintenance(self, *args, **kwargs):
        if 'maintenance_id' in kwargs:
            pk = kwargs['maintenance_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_maintenance(self, vehicle_id, maintenance_type, service_man_id, maintenance_date, paid, kilometer):
        if self.user.has_perm(APP_NAME+".add_manitenance"):
            if service_man_id == 0:
                service_man = None
            else:
                service_man = ServiceMan.objects.get(pk=service_man_id)
            maintenance = Maintenance(vehicle_id=vehicle_id, maintenance_type=maintenance_type,
                                      service_man=service_man, event_time=maintenance_date, paid=paid, kilometer=kilometer)
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
        pass


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
