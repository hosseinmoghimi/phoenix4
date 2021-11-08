from django.shortcuts import render
from core.views import CoreContext
from vehicles.enums import MaintenanceEnum, WorkEventEnum
from vehicles.forms import AddDriverForm, AddMaintenanceForm, AddTripForm, AddVehicleForm, AddVehicleWorkEventForm, AddWorkShiftForm, FilterTripsForm
from vehicles.repo import AreaRepo, DriverRepo, MaintenanceRepo, PassengerRepo, ServiceManRepo, TripPathRepo, TripRepo, VehicleRepo, VehicleWorkEventRepo, WorkShiftRepo
from vehicles.serializers import AreaSerializer, DriverSerializer, MaintenanceSerializer, PassengerSerilizer, ServiceManSerializer, TripPathSerializer, TripSerializer, VehicleSerializer, VehicleWorkEventSerializer, WorkShiftSerializer
from .apps import APP_NAME
from django.views import View
import json

TEMPLATE_FOLDER="vehicles/"
LAYOUT_PARENT="phoenix/layout.html"

# @login_required
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
        
        trip_paths=TripPathRepo(request=request).list()
        context['trip_paths']=trip_paths
        context['trip_paths_s']=json.dumps(TripPathSerializer(trip_paths,many=True).data)

        vehicles=VehicleRepo(request=request).list()
        context['vehicles_s']=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles']=vehicles 
        areas=AreaRepo(request=request).list(*args, **kwargs)
        context['areas']=areas


        
        service_mans=ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans

        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        context['drivers_s']=json.dumps(DriverSerializer(drivers,many=True).data)
 

        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        context['trips_s']=json.dumps(TripSerializer(trips,many=True).data)
        if request.user.has_perm(APP_NAME+".add_trip"):
            context['add_trip_form']=AddTripForm()

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


        
        maintenances=MaintenanceRepo(request=request).list(*args, **kwargs)
        context['maintenances']=maintenances
        maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
        context['maintenances_s']=maintenances_s
        if request.user.has_perm(APP_NAME+".add_maintenance"):
            context['add_maintenance_form']=AddMaintenanceForm()
        

        
        work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s



        
        vehicle_work_events=VehicleWorkEventRepo(request=request).list(*args, **kwargs)
        context['vehicle_work_events']=vehicle_work_events
        vehicle_work_events_s=json.dumps(VehicleWorkEventSerializer(vehicle_work_events,many=True).data)
        context['vehicle_work_events_s']=vehicle_work_events_s


        
        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        context['trips_s']=json.dumps(TripSerializer(trips,many=True).data)
        if request.user.has_perm(APP_NAME+".add_trip"):
            context['add_trip_form']=AddTripForm()


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


    def vehicles(self,request,*args, **kwargs):
        context=getContext(request=request)


        vehicles=VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles 
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s


        if request.user.has_perm(APP_NAME+".add_vehicle"):
            context['add_vehicle_form']=AddVehicleForm()

         
        return render(request,TEMPLATE_FOLDER+"vehicles.html",context)


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


class PassengerViews(View):
    def passenger(self,request,*args, **kwargs):
        context=getContext(request=request)
        passenger=PassengerRepo(request=request).passenger(*args, **kwargs)
        context['passenger']=passenger
        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        trips_s=json.dumps(TripSerializer(trips,many=True).data)
        context['trips_s']=trips_s
        return render(request,TEMPLATE_FOLDER+"passenger.html",context)


class TripViews(View):
    def trip(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip=TripRepo(request=request).trip(*args, **kwargs)
        context['trip']=trip
        context['vehicle']=trip.vehicle
        passengers=trip.passengers.all()
        context['passengers']=passengers
        passengers_s=json.dumps(PassengerSerilizer(passengers,many=True).data)
        context['passengers_s']=passengers_s
        all_passengers=PassengerRepo(request=request).list()
        context['all_passengers']=all_passengers
        all_passengers_s=json.dumps(PassengerSerilizer(all_passengers,many=True).data)
        context['all_passengers_s']=all_passengers_s

        return render(request,TEMPLATE_FOLDER+"trip.html",context)
    def trips(self,request,*args, **kwargs):
        context=getContext(request=request)
        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        trips_s=json.dumps(TripSerializer(trips,many=True).data)
        context['trips_s']=trips_s
        context['filter_trips_form']=FilterTripsForm()
        return render(request,TEMPLATE_FOLDER+"trips.html",context)
    def add_trip_context(self,request,*args, **kwargs):
        context={}

        vehicles=VehicleRepo(request=request).list(*args, **kwargs)
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s

        passengers=PassengerRepo(request=request).list(*args, **kwargs)
        passengers_s=json.dumps(PassengerSerilizer(passengers,many=True).data)
        context['passengers_s']=passengers_s

        
        drivers=DriverRepo(request=request).list(*args, **kwargs)
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s

        paths=TripPathRepo(request=request).list(*args, **kwargs)
        paths_s=json.dumps(TripPathSerializer(paths,many=True).data)
        context['paths_s']=paths_s
        return context

    def trip_path(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip_path=TripPathRepo(request=request).trip_path(*args, **kwargs)
        context['trip_path']=trip_path
        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        trips_s=json.dumps(TripSerializer(trips,many=True).data)
        context['trips_s']=trips_s
        context['add_trip_form']=AddTripForm()
        context.update(self.add_trip_context(request=request))
        return render(request,TEMPLATE_FOLDER+"trip-path.html",context)


class VehicleWorkEventViews(View):
    def vehicle_work_event(self,request,*args, **kwargs):
        context=getContext(request=request)

        vehicle_work_event=VehicleWorkEventRepo(request=request).vehicle_work_event(*args, **kwargs)
        context['vehicle_work_event']=vehicle_work_event
        
        # work_shifts=WorkShiftRepo(request=request).list(vehicle_work_event_id=vehicle_work_event.id)
        work_shifts=[vehicle_work_event.work_shift]
        context['work_shifts']=work_shifts 
        context['work_shifts_s']=json.dumps(WorkShiftSerializer(work_shifts,many=True).data) 
        # context['add_work_shift_form']=1

        return render(request,TEMPLATE_FOLDER+"vehicle-work-event.html",context)


class WorkShiftViews(View):
    def work_shift(self,request,*args, **kwargs):
        context=getContext(request=request)


        area=AreaRepo(request=request).area(*args, **kwargs)
        context['area']=area

        


        context['event_types']=(i[0] for i in WorkEventEnum.choices)
        
        work_shift=WorkShiftRepo(request=request).work_shift(*args, **kwargs)
        context['work_shift']=work_shift 
        
        vehicle_work_events=VehicleWorkEventRepo(request=request).list(work_shift_id=work_shift.id)

        context['vehicle_work_events']=vehicle_work_events
        context['vehicle_work_events_s']=json.dumps(VehicleWorkEventSerializer(vehicle_work_events,many=True).data)
        
        if request.user.has_perm(APP_NAME+".add_vehicleworkevent"):
            context['add_vehicle_work_event_form']=AddVehicleWorkEventForm()

        return render(request,TEMPLATE_FOLDER+"work-shift.html",context)


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


        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        context['trips_s']=json.dumps(TripSerializer(trips,many=True).data)
        if request.user.has_perm(APP_NAME+".add_trip"):
            context['add_trip_form']=AddTripForm()

        
        work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s
        

        return render(request,TEMPLATE_FOLDER+"driver.html",context)

    def drivers(self,request,*args, **kwargs):
        context=getContext(request=request)


        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        context['drivers_s']=json.dumps(DriverSerializer(drivers,many=True).data)
 
        if request.user.has_perm(APP_NAME+".add_driver"):
            context['add_friver_form']=AddDriverForm()

         

        return render(request,TEMPLATE_FOLDER+"drivers.html",context)


class ServiceManViews(View):
    def service_man(self,request,*args, **kwargs):
        context=getContext(request=request)


        service_man=ServiceManRepo(request=request).service_man(*args, **kwargs)
        context['service_man']=service_man

        maintenances=MaintenanceRepo(request=request).list(*args, **kwargs)
        context['maintenances_s']=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
            
    
        return render(request,TEMPLATE_FOLDER+"service-man.html",context)