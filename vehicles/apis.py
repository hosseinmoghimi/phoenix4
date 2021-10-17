
from utility.persian import PersianCalendar
from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from django.http import JsonResponse

from vehicles.repo import MaintenanceRepo, TripRepo, VehicleRepo, WorkShiftRepo
from vehicles.serializers import MaintenanceSerializer, TripSerializer, VehicleSerializer, WorkShiftSerializer
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
                
                name=add_vehicle_form.cleaned_data['name']
                vehicle=VehicleRepo(request=request).add_vehicle(
                    name=name,
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
                trip=TripRepo(request=request).add_trip(
                    title=title,
                )
                
                if trip is not None:
                    log=4
                    context['trip']=TripSerializer(trip).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    