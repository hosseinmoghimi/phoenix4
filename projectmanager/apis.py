from utility.persian import PersianCalendar
from projectmanager.serializers import EmployeeSerializer, EventSerializer, MaterialRequestSerializer,EmployerSerializer, MaterialSerializer, OrganizationUnitSerializer, LocationSerializer, ProjectSerializer, RequestSignatureSerializer, ServiceRequestSerializer, ServiceSerializer, WareHouseSheetSerializer
from core.constants import SUCCEED,FAILED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import EmployerRepo, EventRepo, LocationRepo, MaterialRepo, MaterialRequestRepo, OrganizationUnitRepo, ProjectRepo, ServiceRepo, ServiceRequestRepo, WareHouseSheetRepo
from .forms import *


class LocationApi(APIView):
    def add_location(self,request):
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_location_form=AddLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                location=add_location_form.cleaned_data['location']
                title=add_location_form.cleaned_data['title']
                page_id=add_location_form.cleaned_data['page_id']
                location=LocationRepo(request=request).add_location(page_id=page_id,location=location,title=title)
                
                if location is not None:
                    log=4
                    location_s=LocationSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})
    
    def add_existing_location(self,request):
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_existing_location_form=AddExistingLocationForm(request.POST)
            if add_existing_location_form.is_valid():
                log=3
                location_id=add_existing_location_form.cleaned_data['location_id']
                page_id=add_existing_location_form.cleaned_data['page_id']
                location=LocationRepo(request=request).add_existing_location(page_id=page_id,location_id=location_id)
                
                if location is not None:
                    log=4
                    location_s=LocationSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})
    

class ProjectApi(APIView):
    def add_location(self,request):
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_location_form=AddLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                location=add_location_form.cleaned_data['location']
                title=add_location_form.cleaned_data['title']
                project_id=add_location_form.cleaned_data['page_id']
                location=ProjectRepo(request=request).add_location(project_id=project_id,location=location,title=title)
                if location is not None:
                    log=4
                    location_s=LocationSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})

    def add_project(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_project_form=AddProjectForm(request.POST)
            if add_project_form.is_valid():
                log+=1
                title=add_project_form.cleaned_data['title']
                parent_id=add_project_form.cleaned_data['parent_id']
                project=ProjectRepo(request=request).add_project(parent_id=parent_id,title=title)
                if project is not None:
                    context['project']=ProjectSerializer(project).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def edit_project(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            
            edit_project_form=EditProjectForm(request.POST)
            if edit_project_form.is_valid():
                log+=1
                archive=edit_project_form.cleaned_data['archive']
                title=edit_project_form.cleaned_data['title']
                project_id=edit_project_form.cleaned_data['project_id']
                percentage_completed=edit_project_form.cleaned_data['percentage_completed']
                start_date=edit_project_form.cleaned_data['start_date']
                end_date=edit_project_form.cleaned_data['end_date']
                status=edit_project_form.cleaned_data['status']
                employer_id=edit_project_form.cleaned_data['employer_id']
                weight=edit_project_form.cleaned_data['weight']
                contractor_id=edit_project_form.cleaned_data['contractor_id']
                
                start_date=PersianCalendar().to_gregorian(start_date)
                end_date=PersianCalendar().to_gregorian(end_date)
                project=ProjectRepo(request=request).edit_project(weight=weight,title=title,archive=archive,contractor_id=contractor_id,employer_id=employer_id,project_id=project_id,percentage_completed=percentage_completed,start_date=start_date,end_date=end_date,status=status)
                if project is not None: 
                    context['project']=ProjectSerializer(project).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def add_signature(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_signature_form=AddSignatureForm(request.POST)
            if add_signature_form.is_valid():
                log+=1
                status=add_signature_form.cleaned_data['status']
                description=add_signature_form.cleaned_data['description']
                material_request_id=add_signature_form.cleaned_data['material_request_id']
                service_request_id=add_signature_form.cleaned_data['service_request_id']
                if material_request_id is not None:
                    signature=MaterialRequestRepo(request=request).add_signature(material_request_id=material_request_id,status=status,description=description)
                    context['signature']=RequestSignatureSerializer(signature).data
                    context['result']=SUCCEED
                if service_request_id is not None:
                    signature=ServiceRequestRepo(request=request).add_signature(service_request_id=service_request_id,status=status,description=description)
                    context['signature']=RequestSignatureSerializer(signature).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class EventApi(APIView):
    def add_event(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_event_form=AddEventForm(request.POST)
            if add_event_form.is_valid():
                log+=1
                title=add_event_form.cleaned_data['title']
                event_datetime=add_event_form.cleaned_data['event_datetime']
                start_datetime=add_event_form.cleaned_data['start_datetime']
                end_datetime=add_event_form.cleaned_data['end_datetime']
                project_id=add_event_form.cleaned_data['project_id']
                event_datetime=PersianCalendar().to_gregorian(event_datetime)
                start_datetime=PersianCalendar().to_gregorian(start_datetime)
                end_datetime=PersianCalendar().to_gregorian(end_datetime)
                event=EventRepo(request=request).add_event(start_datetime=start_datetime,end_datetime=end_datetime,event_datetime=event_datetime,project_id=project_id,title=title)
                if event is not None:
                    context['event']=EventSerializer(event).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class OrganizationUnitApi(APIView):
    def add_organization_unit(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_organization_unit_form=AddOrganizationUnitForm(request.POST)
            if add_organization_unit_form.is_valid():
                log+=1
                organization_unit_id=add_organization_unit_form.cleaned_data['organization_unit_id']
                project_id=add_organization_unit_form.cleaned_data['project_id']
                title=add_organization_unit_form.cleaned_data['title']
                parent_id=add_organization_unit_form.cleaned_data['parent_id']
                employer_id=add_organization_unit_form.cleaned_data['employer_id']
                if organization_unit_id is not None and project_id is not None:
                    organization_unit=ProjectRepo(request=request).add_organization_unit(organization_unit_id=organization_unit_id,project_id=project_id)
                else:
                    organization_unit=OrganizationUnitRepo(request=request).add_organization_unit(parent_id=parent_id,employer_id=employer_id,title=title)
                if organization_unit is not None:
                    context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def add_employer(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_employer_form=AddEmployerForm(request.POST)
            if add_employer_form.is_valid():
                log+=1
                title=add_employer_form.cleaned_data['title']
                employer=EmployerRepo(request=request).add_employer(title=title)
                if employer is not None:
                    context['employer']=EmployerSerializer(employer).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_employee(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_employee_form=AddEmployeeForm(request.POST)
            if add_employee_form.is_valid():
                log+=1
                first_name=add_employee_form.cleaned_data['first_name']
                last_name=add_employee_form.cleaned_data['last_name']
                username=add_employee_form.cleaned_data['username']
                password=add_employee_form.cleaned_data['password']
                organization_unit_id=add_employee_form.cleaned_data['organization_unit_id']
                profile_id=add_employee_form.cleaned_data['profile_id']
                employee=OrganizationUnitRepo(request=request).add_employee(username=username,password=password,first_name=first_name,last_name=last_name,profile_id=profile_id,organization_unit_id=organization_unit_id)
                if employee is not None:
                    context['employee']=EmployeeSerializer(employee).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class WareHouseSheetApi(APIView):
    def add_material_request_to_ware_house_sheet(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_material_request_to_ware_house_sheet_form=AddMaterialRequestToWareHouseSheetForm(request.POST)
            if add_material_request_to_ware_house_sheet_form.is_valid():
                log+=1
                ware_house_sheet_id=add_material_request_to_ware_house_sheet_form.cleaned_data['ware_house_sheet_id']
                material_request_id=add_material_request_to_ware_house_sheet_form.cleaned_data['material_request_id']
                ware_house_id=add_material_request_to_ware_house_sheet_form.cleaned_data['ware_house_id']
                date_exported=add_material_request_to_ware_house_sheet_form.cleaned_data['date_exported']
                
                date_exported=PersianCalendar().to_gregorian(date_exported)
                ware_house_sheet=WareHouseSheetRepo(request=request).add_material_request_to_ware_house_sheet(
                    material_request_id=material_request_id,
                    ware_house_id=ware_house_id,
                    ware_house_sheet_id=ware_house_sheet_id,
                    )

                if ware_house_sheet is not None:
                    context['ware_house_sheet']=WareHouseSheetSerializer(ware_house_sheet).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class MaterialApi(APIView):

    def add_material(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_material_form=AddMaterialForm(request.POST)
            if add_material_form.is_valid():
                log+=1
                title=add_material_form.cleaned_data['title']
                parent_id=add_material_form.cleaned_data['parent_id']
                material=MaterialRepo(request=request).add_material(parent_id=parent_id,title=title)
                if material is not None:
                    context['material']=MaterialSerializer(material).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class MaterialRequestApi(APIView):
    def add_material_request(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_material_request_form=AddMaterialRequestForm(request.POST)
            if add_material_request_form.is_valid():
                log+=1
                material_id=add_material_request_form.cleaned_data['material_id']
                # material_title=add_material_request_form.cleaned_data['material_title']
                employee_id=add_material_request_form.cleaned_data['employee_id']
                project_id=add_material_request_form.cleaned_data['project_id']
                quantity=add_material_request_form.cleaned_data['quantity']
                unit_name=add_material_request_form.cleaned_data['unit_name']
                unit_price=add_material_request_form.cleaned_data['unit_price']
                material_request=MaterialRequestRepo(request=request).add_material_request(employee_id=employee_id,unit_price=unit_price,unit_name=unit_name,quantity=quantity,material_id=material_id,project_id=project_id)
                # ware_house_sheet=WareHouseSheetRepo(request=request).add_sheet(material_request=material_request)
                if material_request is not None:
                    context['material_request']=MaterialRequestSerializer(material_request).data
                    # context['ware_house_sheet']=WareHouseSheetSerializer(ware_house_sheet).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class ServiceRequestApi(APIView):
    def add_service_request(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_service_request_form=AddServiceRequestForm(request.POST)
            if add_service_request_form.is_valid():
                log+=1
                service_title=add_service_request_form.cleaned_data['service_title']
                employee_id=add_service_request_form.cleaned_data['employee_id']
                project_id=add_service_request_form.cleaned_data['project_id']
                quantity=add_service_request_form.cleaned_data['quantity']
                unit_name=add_service_request_form.cleaned_data['unit_name']
                unit_price=add_service_request_form.cleaned_data['unit_price']
                service_request=ServiceRequestRepo(request=request).add_service_request(employee_id=employee_id,unit_price=unit_price,unit_name=unit_name,quantity=quantity,service_title=service_title,project_id=project_id)
                if service_request is not None:
                    context['service_request']=ServiceRequestSerializer(service_request).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_service(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_service_form=AddServiceForm(request.POST)
            if add_service_form.is_valid():
                log+=1
                title=add_service_form.cleaned_data['title']
                parent_id=add_service_form.cleaned_data['parent_id']
                service=ServiceRepo(request=request).add_service(title=title,parent_id=parent_id)
                if service is not None:
                    context['service']=ServiceSerializer(service).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class ServiceApi(APIView):
    def add_service(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_service_form=AddServiceForm(request.POST)
            if add_service_form.is_valid():
                log+=1
                title=add_service_form.cleaned_data['title']
                parent_id=add_service_form.cleaned_data['parent_id']
                service=ServiceRepo(request=request).add_service(title=title,parent_id=parent_id)
                if service is not None:
                    context['service']=ServiceSerializer(service).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

