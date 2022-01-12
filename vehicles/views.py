from datetime import datetime
from django.http.response import Http404
from django.utils import timezone
from projectmanager.repo import LocationRepo
from django.shortcuts import render
from authentication.repo import ProfileRepo
from authentication.serializers import ProfileSerializer
from core.views import CoreContext, MessageView
from utility.persian import PersianCalendar
from vehicles.enums import MaintenanceEnum, WorkEventEnum
from vehicles.forms import *
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
    me_passenger=PassengerRepo(request=request).me
    context['me_passenger']=me_passenger
 
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
        context['areas_s']=json.dumps(AreaSerializer(areas,many=True).data)


        
        service_mans=ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans
        context['service_mans_s']=json.dumps(ServiceManSerializer(service_mans,many=True).data)

        drivers=DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        context['drivers_s']=json.dumps(DriverSerializer(drivers,many=True).data)
 

        passengers=PassengerRepo(request=request).list(*args, **kwargs)
        context['passengers']=passengers
        all_passengers_s=json.dumps(PassengerSerilizer(passengers,many=True).data)
        context['passengers_s']=all_passengers_s
        context['all_passengers_s']=all_passengers_s
 

        trips=TripRepo(request=request).list(*args, **kwargs)
        context['trips']=trips
        context['trips_s']=json.dumps(TripSerializer(trips,many=True).data)
        if request.user.has_perm(APP_NAME+".add_trip"):
            context['add_trip_form']=AddTripForm()

        return render(request,TEMPLATE_FOLDER+"index.html",context)


class VehicleViews(View): 
    def vehicle_report(self,request,*args, **kwargs):
        if request.method=='POST':
            my_form=VehicleReportForm(request.POST)
            if my_form.is_valid():
                from utility.persian import PERSIAN_MONTH_NAMES,days_in_month,JalaliDate
                cd=my_form.cleaned_data
                vehicle_id=cd['vehicle_id']
                month=cd['month']
                year=cd['year'] 
                start_date=str(JalaliDate(year=year,month=month)).replace('-','/')
                end_date=str(JalaliDate(year=year,month=month,day=days_in_month(year=year,month=month))).replace('-','/')
                start_date=PersianCalendar().to_gregorian(start_date)
                end_date=PersianCalendar().to_gregorian(end_date)

                context=getContext(request=request)


                context['year']=year

                months=[]
                for i in range(12):
                    months.append({'number':i+1,'name':PERSIAN_MONTH_NAMES[i]})
                context['months']=months
                context['month']=month
                context['month_number']=int(month)
                context['month_name']=PERSIAN_MONTH_NAMES[int(month)-1]
                context['vehicle_report_form']=VehicleReportForm()
                

                context['start_date']=start_date
                context['end_date']=end_date
                vehicle=VehicleRepo(request=request).vehicle(vehicle_id=vehicle_id)
                context['vehicle']=vehicle
        
                ##
                maintenances=MaintenanceRepo(request=request).list(*args, **kwargs).filter(vehicle_id=vehicle_id).filter(event_datetime__gte=start_date).filter(event_datetime__lte=end_date)
                context['maintenances']=maintenances
                maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
                context['maintenances_s']=maintenances_s
            
                ##
                work_shifts=WorkShiftRepo(request=request).list(*args, **kwargs).filter(vehicle_id=vehicle_id).filter(start_time__gte=start_date).filter(start_time__lte=end_date)
                context['work_shifts']=work_shifts
                work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
                context['work_shifts_s']=work_shifts_s



                ##
                vehicle_work_events=VehicleWorkEventRepo(request=request).list(*args, **kwargs).filter(vehicle_id=vehicle_id).filter(event_datetime__gte=start_date).filter(event_datetime__lte=end_date)
                context['vehicle_work_events']=vehicle_work_events
                vehicle_work_events_s=json.dumps(VehicleWorkEventSerializer(vehicle_work_events,many=True).data)
                context['vehicle_work_events_s']=vehicle_work_events_s

                ##
                trips=TripRepo(request=request).list(*args, **kwargs).filter(vehicle_id=vehicle_id).filter(date_started__gte=start_date).filter(date_started__lte=end_date)
                context['trips']=trips
                context['trips_s']=json.dumps(TripSerializer(trips,many=True).data)
        
                return render(request,TEMPLATE_FOLDER+"vehicle-report.html",context)

    
    
    def vehicle(self,request,*args, **kwargs):
        context=getContext(request=request)

        now=PersianCalendar().from_gregorian(timezone.now())
        month=now[5:7]
        year=now[:4]
        context['year']=year

        from utility.persian import PERSIAN_MONTH_NAMES
        months=[]
        for i in range(12):
            months.append({'number':i+1,'name':PERSIAN_MONTH_NAMES[i]})
        context['months']=months
        context['month']=month
        context['month_number']=int(month)
        context['month_name']=PERSIAN_MONTH_NAMES[int(month)-1]
        context['vehicle_report_form']=VehicleReportForm()


        context['vehicle_report_form']=VehicleReportForm()

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
        if request.user.has_perm(APP_NAME+".add_vehicleworkevent"):
            context['event_types']=(i[0] for i in WorkEventEnum.choices)
            work_shifts=WorkShiftRepo(request=request).list(vehicle_id=vehicle.id).order_by("-start_time")
            context['work_shifts']=work_shifts
            context['add_vehicle_work_event_form']=AddVehicleWorkEventForm()
        


        
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

    def areas(self,request,*args, **kwargs):
        context=getContext(request=request)


        areas=AreaRepo(request=request).list(*args, **kwargs)
        context['areas']=areas
        areas_s=json.dumps(AreaSerializer(areas,many=True).data)
        context['areas_s']=areas_s
        if request.user.has_perm(APP_NAME+".add_area"):
            context['add_area_form']=AddAreaForm()
 
        return render(request,TEMPLATE_FOLDER+"areas.html",context)


class PassengerViews(View):
    def passengers(self,request,*args, **kwargs):
        context=getContext(request=request)
        passengers=PassengerRepo(request=request).list(*args, **kwargs)
        context['passengers']=passengers
        passengers_s=json.dumps(PassengerSerilizer(passengers,many=True).data)
        context['passengers_s']=passengers_s
        context['all_passengers_s']=passengers_s
        if request.user.has_perm(APP_NAME+'.add_driver'):
            context['add_passenger_form']=AddPassengerForm()
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles
            context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
        return render(request,TEMPLATE_FOLDER+"passengers.html",context)

    def passenger(self,request,*args, **kwargs):
        context=getContext(request=request)
        passenger=PassengerRepo(request=request).passenger(*args, **kwargs)
        me_passenger=PassengerRepo(request=request).me
        if request.user.has_perm(APP_NAME+".view_passenger"):
            pass
        elif passenger==me_passenger:
            # print(me_passenger)
            pass
        else:
            header_text="دسترسی غیر مجاز برای شما"
            mm=MessageView(request=request,header_text=header_text)
            return mm.response()

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
        me_driver=DriverRepo(request=request).me
        me_passenger=PassengerRepo(request=request).me
        if request.user.has_perm(APP_NAME+".view_trip"):
            pass
        elif trip.driver==me_driver:
            pass
        elif me_passenger is not None and me_passenger in trip.passengers.all():
            pass
        else:
            header_text="دسترسی غیر مجاز برای شما"
            mm=MessageView(request=request,header_text=header_text)
            return mm.response()

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
        context['add_passenger_to_trip_form']=AddPassengerToTripForm()
        return render(request,TEMPLATE_FOLDER+"trip.html",context)

        
    def trip_request(self,request,*args, **kwargs):
        context=getContext(request=request)
        me_passenger=context['me_passenger']
        if me_passenger is None and not request.user.has_perm(APP_NAME+"add_trip"):
            raise Http404
        if me_passenger is None:
            context['passenger_id']=0
        else:
            context['passenger_id']=me_passenger.id


        context.update(self.add_trip_context(request=request,*args, **kwargs))
        me_passenger=context['me_passenger']
        if me_passenger is not None:
            context['me_passenger_s']=json.dumps(PassengerSerilizer(me_passenger).data)

        context['add_trip_form']=AddTripForm()
        return render(request,TEMPLATE_FOLDER+"trip-request.html",context)

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

        all_passengers=PassengerRepo(request=request).list(*args, **kwargs)
        all_passengers_s=json.dumps(PassengerSerilizer(all_passengers,many=True).data)
        context['all_passengers_s']=all_passengers_s

        
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

    def trip_paths(self,request,*args, **kwargs):
        context=getContext(request=request)
        trip_paths=TripPathRepo(request=request).list(*args, **kwargs)
        context['trip_paths']=trip_paths
        trip_paths_s=json.dumps(TripPathSerializer(trip_paths,many=True).data)
        context['trip_paths_s']=trip_paths_s

        locations=LocationRepo(request=request).list(*args, **kwargs)
        context['locations']=locations

        if request.user.has_perm(APP_NAME+".add_trippath"):
            context['add_trip_path_form']=AddTripPathForm()
            
        return render(request,TEMPLATE_FOLDER+"trip-paths.html",context)


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
        me_driver=DriverRepo(request=request).me
        if request.user.has_perm(APP_NAME+".view_driver"):
            pass
        elif driver==me_driver:
            # print(me_driver)
            pass
        else:
            header_text="دسترسی غیر مجاز برای شما"
            mm=MessageView(request=request,header_text=header_text)
            return mm.response()

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
            context['add_driver_form']=AddDriverForm()
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles
            context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
         

        return render(request,TEMPLATE_FOLDER+"drivers.html",context)


class ServiceManViews(View):
    def service_man(self,request,*args, **kwargs):
        context=getContext(request=request)


        service_man=ServiceManRepo(request=request).service_man(*args, **kwargs)
        context['service_man']=service_man

        maintenances=MaintenanceRepo(request=request).list(*args, **kwargs)
        context['maintenances_s']=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
        me_service_man=ServiceManRepo(request=request).me
        if request.user.has_perm(APP_NAME+".view_serviceman"):
            pass
        elif me_service_man is not None and service_man.id==me_service_man.id:
            pass
        else:
            header_text="دسترسی غیر مجاز برای شما"
            mm=MessageView(request=request,header_text=header_text)
            return mm.response()

            
    
        return render(request,TEMPLATE_FOLDER+"service-man.html",context)
    def service_mans(self,request,*args, **kwargs):
        context=getContext(request=request)


        service_mans=ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans
        context['service_mans_s']=json.dumps(ServiceManSerializer(service_mans,many=True).data)
        if request.user.has_perm(APP_NAME+".add_serviceman"):
            context['add_serviceman_form']=AddServiceManForm()
            profiles=ProfileRepo(request=request).list()
            context['profiles']=profiles
            context['profiles_s']=json.dumps(ProfileSerializer(profiles,many=True).data)
         

            
    
        return render(request,TEMPLATE_FOLDER+"service-mans.html",context)