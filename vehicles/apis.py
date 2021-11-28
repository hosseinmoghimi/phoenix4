
from django.utils import timezone
from utility.persian import PersianCalendar
from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
import json
from vehicles.repo import DriverRepo, MaintenanceRepo, TripPathRepo, TripRepo, VehicleRepo, VehicleWorkEventRepo, WorkShiftRepo
from vehicles.serializers import DriverSerializer, MaintenanceSerializer, PassengerSerilizer, TripPathSerializer, TripSerializer, VehicleSerializer, VehicleWorkEventSerializer, WorkShiftSerializer
from .forms import *


class WorkShiftApi(APIView):
    def add_work_shift(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_work_shift_form=AddWorkShiftForm(request.POST)
            if add_work_shift_form.is_valid():
                log=3
                
                driver_id=add_work_shift_form.cleaned_data['driver_id']
                vehicle_id=add_work_shift_form.cleaned_data['vehicle_id']
                start_datetime=add_work_shift_form.cleaned_data['start_datetime']
                end_datetime=add_work_shift_form.cleaned_data['end_datetime']
                area_id=add_work_shift_form.cleaned_data['area_id']
                description=add_work_shift_form.cleaned_data['description']
                income=add_work_shift_form.cleaned_data['income']
                outcome=add_work_shift_form.cleaned_data['outcome']
                end_datetime=PersianCalendar().to_gregorian(end_datetime)
                start_datetime=PersianCalendar().to_gregorian(start_datetime)
                work_shift=WorkShiftRepo(request=request).add_work_shift(
                    area_id=area_id,
                    income=income,
                    outcome=outcome,
                    description=description,
                    driver_id=driver_id,
                    vehicle_id=vehicle_id,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime)
                
                if work_shift is not None:
                    log=4
                    work_shift=WorkShiftSerializer(work_shift).data
                    context['work_shift']=work_shift
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    

class VehicleWorkEventApi(APIView):
    def add_vehicle_work_event(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_vehicle_work_event_form=AddVehicleWorkEventForm(request.POST)
            if add_vehicle_work_event_form.is_valid():
                log=3
                
                work_shift_id=add_vehicle_work_event_form.cleaned_data['work_shift_id']
                event_type=add_vehicle_work_event_form.cleaned_data['event_type']
                vehicle_id=add_vehicle_work_event_form.cleaned_data['vehicle_id']
                event_datetime=add_vehicle_work_event_form.cleaned_data['event_datetime']
                kilometer=add_vehicle_work_event_form.cleaned_data['kilometer']
                description=add_vehicle_work_event_form.cleaned_data['description']

              
                event_datetime=PersianCalendar().to_gregorian(event_datetime)
                vehicle_work_event=VehicleWorkEventRepo(request=request).add_vehicle_work_event(
                    work_shift_id=work_shift_id,
                    event_type=event_type,
                    event_datetime=event_datetime,
                    description=description,
                    kilometer=kilometer,
                    )
                
                if vehicle_work_event is not None:
                    log=4
                    vehicle_work_event=VehicleWorkEventSerializer(vehicle_work_event).data
                    context['vehicle_work_event']=vehicle_work_event
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    

class MaintenanceApi(APIView):
    def add_maintenance(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_maintenance_form=AddMaintenanceForm(request.POST)
            if add_maintenance_form.is_valid():
                log=3
                
                title=add_maintenance_form.cleaned_data['title']
                vehicle_id=add_maintenance_form.cleaned_data['vehicle_id']
                event_datetime=add_maintenance_form.cleaned_data['event_datetime']
                kilometer=add_maintenance_form.cleaned_data['kilometer']
                paid=add_maintenance_form.cleaned_data['paid']
                description=add_maintenance_form.cleaned_data['description']
                service_man_id=add_maintenance_form.cleaned_data['service_man_id']
                maintenance_type=add_maintenance_form.cleaned_data['maintenance_type']
                event_datetime=PersianCalendar().to_gregorian(event_datetime)
                maintenance=MaintenanceRepo(request=request).add_maintenance(
                    paid=paid,
                    service_man_id=service_man_id,
                    maintenance_type=maintenance_type,
                    description=description,
                    title=title,
                    vehicle_id=vehicle_id,
                    event_datetime=event_datetime,
                    kilometer=kilometer)
                
                if maintenance is not None:
                    log=4
                    maintenance=MaintenanceSerializer(maintenance).data
                    context['maintenance']=maintenance
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
class VehicleApi(APIView):
    def add_new_vehicle(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_vehicle_form=AddVehicleForm(request.POST)
            if add_vehicle_form.is_valid():
                log=3
                
                title=add_vehicle_form.cleaned_data['title']
                vehicle=VehicleRepo(request=request).add_vehicle(
                    title=title,
                )
                
                if vehicle is not None:
                    log=4
                    context['vehicle']=VehicleSerializer(vehicle).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
class TripApi(APIView):
    def add_new_trip(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_trip_form=AddTripForm(request.POST)
            if add_trip_form.is_valid():
                log=3
                
                title=add_trip_form.cleaned_data['title']
                vehicle_id=add_trip_form.cleaned_data['vehicle_id']
                driver_id=add_trip_form.cleaned_data['driver_id']
                paths=add_trip_form.cleaned_data['paths']
                cost=add_trip_form.cleaned_data['cost']
                delay=add_trip_form.cleaned_data['delay']
                passengers=add_trip_form.cleaned_data['passengers']
                start_datetime=add_trip_form.cleaned_data['start_datetime']
                end_datetime=add_trip_form.cleaned_data['end_datetime']
                if start_datetime is None or start_datetime=="":
                    start_datetime=timezone.now()
                else:
                    start_datetime=PersianCalendar().from_gregorian(start_datetime)
                
                if end_datetime is None or end_datetime=="":
                    end_datetime=timezone.now()
                else:
                    end_datetime=PersianCalendar().from_gregorian(end_datetime)
                paths=json.loads(paths)
                passengers=json.loads(passengers)
                trip=TripRepo(request=request).add_trip(
                    title=title,
                    vehicle_id=vehicle_id,
                    driver_id=driver_id,
                    paths=paths,
                    cost=cost,
                    delay=delay,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    passengers=passengers,
                )
                
                if trip is not None:
                    log=4
                    context['trip']=TripSerializer(trip).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def add_trip_path(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_trip_path_form=AddTripPathForm(request.POST)
            if add_trip_path_form.is_valid():
                log=3
                
                source_id=add_trip_path_form.cleaned_data['source_id']
                destination_id=add_trip_path_form.cleaned_data['destination_id']
                duration=add_trip_path_form.cleaned_data['duration']
                distance=add_trip_path_form.cleaned_data['distance']
                cost=add_trip_path_form.cleaned_data['cost']
                 
                trip_path=TripPathRepo(request=request).add_trip_path(
                    source_id=source_id,
                    destination_id=destination_id,
                    duration=duration,
                    distance=distance,
                    cost=cost,
                )
                
                if trip_path is not None:
                    log=4
                    context['trip_path']=TripPathSerializer(trip_path).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def filter_trip(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            filter_trip_form=FilterTripForm(request.POST)
            if filter_trip_form.is_valid():
                log=3

                title=filter_trip_form.cleaned_data['title']
                vehicle_id=filter_trip_form.cleaned_data['vehicle_id']
                driver_id=filter_trip_form.cleaned_data['driver_id']
                trip_path_id=filter_trip_form.cleaned_data['trip_path_id']
                start_date=filter_trip_form.cleaned_data['start_date']
                end_date=filter_trip_form.cleaned_data['end_date']
                if start_date is None or start_date=="":
                    start_date=timezone.now()
                else:
                    start_date=PersianCalendar().to_gregorian(start_date)
                
                if end_date is None or end_date=="":
                    end_date=timezone.now()
                else:
                    end_date=PersianCalendar().to_gregorian(end_date)
                trips=TripRepo(request=request).list(
                    title=title,
                    vehicle_id=vehicle_id,
                    driver_id=driver_id,
                    trip_path_id=trip_path_id,
                    start_date=start_date,
                    end_date=end_date,
                )
                
                if trips is not None:
                    log=4
                    context['trips']=TripSerializer(trips,many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def add_passenger_to_trip(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_passenger_to_trip_form=AddPassengerToTripForm(request.POST)
            if add_passenger_to_trip_form.is_valid():
                log=3
                
                trip_id=add_passenger_to_trip_form.cleaned_data['trip_id']
                passenger_id=add_passenger_to_trip_form.cleaned_data['passenger_id']
                passenger=TripRepo(request=request).add_passenger_to_trip(
                    passenger_id=passenger_id,
                    trip_id=trip_id,
                )
                
                if passenger is not None:
                    log=4
                    context['passenger']=PassengerSerilizer(passenger).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
class DriverApi(APIView):
    def add_new_driver(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_driver_form=AddDriverForm(request.POST)
            if add_driver_form.is_valid():
                log=3
                
                profile_id=add_driver_form.cleaned_data['profile_id']
              
                driver=DriverRepo(request=request).add_driver(
                    profile_id=profile_id,
                )
                
                if driver is not None:
                    log=4
                    context['driver']=DriverSerializer(driver).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
   