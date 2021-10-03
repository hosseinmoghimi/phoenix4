from django.shortcuts import render
from core.views import CoreContext
from vehicles.enums import MaintenanceEnum
from vehicles.forms import AddMaintenanceForm, AddWorkShiftForm
from vehicles.repo import AreaRepo, DriverRepo, MaintenanceRepo, ServiceManRepo, VehicleRepo, VehicleWorkEventRepo, WorkShiftRepo
from vehicles.serializers import AreaSerializer, DriverSerializer, MaintenanceSerializer, ServiceManSerializer, VehicleWorkEventSerializer, WorkShiftSerializer
from .apps import APP_NAME
from django.views import View
import json


TEMPLATE_FOLDER="vehicles/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    context['app']={
        'home_url':"/vehicles/",
        'title':'ماشین آلات',
    }
    return context


class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)

        vehicles=VehicleRepo(request=request).list()
        context['vehicles']=vehicles

        areas=AreaRepo(request=request).list(*args, **kwargs)
        context['areas']=areas


        
        service_mans=ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans

        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers

        return render(request,TEMPLATE_FOLDER+"index.html",context)



class VehicleViews(View):
    def vehicle(self,request,*args, **kwargs):
        context=getContext(request=request)


        vehicle=VehicleRepo(request=request).vehicle(*args, **kwargs)
        context['vehicle']=vehicle


        
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s


        

        
        work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s



        
        vehicle_work_events=VehicleWorkEventRepo(request=request).list(*args, **kwargs)
        context['vehicle_work_events']=vehicle_work_events
        vehicle_work_events_s=json.dumps(VehicleWorkEventSerializer(vehicle_work_events,many=True).data)
        context['vehicle_work_events_s']=vehicle_work_events_s


        

        if request.user.has_perm(APP_NAME+".add_workshif"):
            context['add_work_shift_form']=AddWorkShiftForm()
            areas=AreaRepo(request=request).list(*args, **kwargs)
            context['areas']=areas
            areas_s=json.dumps(AreaSerializer(areas,many=True).data)
            context['areas_s']=areas_s

        if request.user.has_perm(APP_NAME+".add_maintenance"):
            context['add_maintenance_form']=AddMaintenanceForm()
            context['maintenance_types']=(i[0] for i in MaintenanceEnum.choices)
            maintenances=MaintenanceRepo(request=request).list(*args, **kwargs)
            context['maintenances_s']=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
            
            service_mans=ServiceManRepo(request=request).list(*args, **kwargs)
            context['service_mans']=service_mans
            context['service_mans_s']=json.dumps(ServiceManSerializer(service_mans,many=True).data)


        return render(request,TEMPLATE_FOLDER+"vehicle.html",context)




class AreaViews(View):
    def area(self,request,*args, **kwargs):
        context=getContext(request=request)


        area=AreaRepo(request=request).area(*args, **kwargs)
        context['area']=area


        
        work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s
        

        return render(request,TEMPLATE_FOLDER+"area.html",context)


class MaintenanceViews(View):
    def maintenance(self,request,*args, **kwargs):
        context=getContext(request=request)


        maintenance=MaintenanceRepo(request=request).maintenance(*args, **kwargs)
        context['maintenance']=maintenance


        maintenances=MaintenanceRepo(request=request).list(maintenance_type=maintenance.maintenance_type)
        context['maintenances']=maintenances
        context['maintenances_s']=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
            


        return render(request,TEMPLATE_FOLDER+"maintenance.html",context)


class DriverViews(View):
    def driver(self,request,*args, **kwargs):
        context=getContext(request=request)


        driver=DriverRepo(request=request).driver(*args, **kwargs)
        context['driver']=driver


        
        work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s
        

        return render(request,TEMPLATE_FOLDER+"driver.html",context)
class ServiceManViews(View):
    def service_man(self,request,*args, **kwargs):
        context=getContext(request=request)


        service_man=ServiceManRepo(request=request).service_man(*args, **kwargs)
        context['service_man']=service_man

        maintenances=MaintenanceRepo(request=request).list(*args, **kwargs)
        context['maintenances_s']=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
            
    
        return render(request,TEMPLATE_FOLDER+"service-man.html",context)