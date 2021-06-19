from utility.persian import PersianCalendar
from projectmanager.serializers import EmployeeSerializer, EventSerializer, MaterialRequestSerializer,EmployerSerializer, MaterialRequestSignatureSerializer, MaterialSerializer, OrganizationUnitSerializer, ProjectSerializer, ServiceRequestSerializer, ServiceRequestSignatureSerializer, ServiceSerializer
from core.constants import SUCCEED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import EmployerRepo, EventRepo, MaterialRepo, OrganizationUnitRepo, ProjectRepo, ServiceRepo
from .forms import *



class ProjectApi(APIView):
    def add_project(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_project_form=AddProjectForm(request.POST)
            if add_project_form.is_valid():
                log+=1
                title=add_project_form.cleaned_data['title']
                parent_id=add_project_form.cleaned_data['parent_id']
                project=ProjectRepo(request=request).add_project(parent_id=parent_id,title=title)
                context['project']=ProjectSerializer(project).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def edit_project(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            
            edit_project_form=EditProjectForm(request.POST)
            if edit_project_form.is_valid():
                log+=1
                project_id=edit_project_form.cleaned_data['project_id']
                percentage_completed=edit_project_form.cleaned_data['percentage_completed']
                start_date=edit_project_form.cleaned_data['start_date']
                end_date=edit_project_form.cleaned_data['end_date']
                status=edit_project_form.cleaned_data['status']
                start_date=PersianCalendar().to_gregorian(start_date)
                end_date=PersianCalendar().to_gregorian(end_date)
                project=ProjectRepo(request=request).edit_project(project_id=project_id,percentage_completed=percentage_completed,start_date=start_date,end_date=end_date,status=status)
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
                    signature=MaterialRepo(request=request).add_signature(material_request_id=material_request_id,status=status,description=description)
                    context['signature']=MaterialRequestSignatureSerializer(signature).data
                    context['result']=SUCCEED
                if service_request_id is not None:
                    signature=ServiceRepo(request=request).add_signature(service_request_id=service_request_id,status=status,description=description)
                    context['signature']=ServiceRequestSignatureSerializer(signature).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class EventApi(APIView):
    def add_event(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_event_form=AddEventForm(request.POST)
            if add_event_form.is_valid():
                log+=1
                title=add_event_form.cleaned_data['title']
                event_datetime=add_event_form.cleaned_data['event_datetime']
                project_id=add_event_form.cleaned_data['project_id']
                event=EventRepo(request=request).add_event(event_datetime=event_datetime,project_id=project_id,title=title)
                context['event']=EventSerializer(event).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class OrganizationUnitApi(APIView):
    def add_organization_unit(self,request,*args, **kwargs):
        context={}
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
        log=1
        if request.method=='POST':
            log+=1
            add_employer_form=AddEmployerForm(request.POST)
            if add_employer_form.is_valid():
                log+=1
                title=add_employer_form.cleaned_data['title']
                employer=EmployerRepo(request=request).add_employer(title=title)
                context['employer']=EmployerSerializer(employer).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_employee(self,request,*args, **kwargs):
        context={}
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


class MaterialApi(APIView):
    def add_material_request(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_material_request_form=AddMaterialRequestForm(request.POST)
            if add_material_request_form.is_valid():
                log+=1
                material_id=add_material_request_form.cleaned_data['material_id']
                # material_title=add_material_request_form.cleaned_data['material_title']
                project_id=add_material_request_form.cleaned_data['project_id']
                quantity=add_material_request_form.cleaned_data['quantity']
                unit_name=add_material_request_form.cleaned_data['unit_name']
                unit_price=add_material_request_form.cleaned_data['unit_price']
                material_request=MaterialRepo(request=request).add_material_request(unit_price=unit_price,unit_name=unit_name,quantity=quantity,material_id=material_id,project_id=project_id)
                context['material_request']=MaterialRequestSerializer(material_request).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_material(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_material_form=AddMaterialForm(request.POST)
            if add_material_form.is_valid():
                log+=1
                title=add_material_form.cleaned_data['title']
                parent_id=add_material_form.cleaned_data['parent_id']
                material=MaterialRepo(request=request).add_material(parent_id=parent_id,title=title)
                context['material']=MaterialSerializer(material).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)



class ServiceApi(APIView):
    def add_service_request(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_service_request_form=AddServiceRequestForm(request.POST)
            if add_service_request_form.is_valid():
                log+=1
                service_title=add_service_request_form.cleaned_data['service_title']
                project_id=add_service_request_form.cleaned_data['project_id']
                quantity=add_service_request_form.cleaned_data['quantity']
                unit_name=add_service_request_form.cleaned_data['unit_name']
                unit_price=add_service_request_form.cleaned_data['unit_price']
                service_request=ServiceRepo(request=request).add_service_request(unit_price=unit_price,unit_name=unit_name,quantity=quantity,service_title=service_title,project_id=project_id)
                print(100*"#76553456")
                print(service_request.service.title)
                context['service_request']=ServiceRequestSerializer(service_request).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def add_service(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_service_form=AddServiceForm(request.POST)
            if add_service_form.is_valid():
                log+=1
                title=add_service_form.cleaned_data['title']
                parent_id=add_service_form.cleaned_data['parent_id']
                service=ServiceRepo(request=request).add_service(title=title,parent_id=parent_id)
                context['service']=ServiceSerializer(service).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

