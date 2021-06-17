from django.http import request
from projectmanager.enums import RequestStatusEnum, SignatureStatusEnum, UnitNameEnum
from authentication.repo import ProfileRepo
from authentication.models import Profile
from projectmanager.serializers import MaterialRequestSerializer, MaterialSerializer, ServiceRequestSignatureSerializer
from django.db.models.query_utils import Q
from .apps import APP_NAME
from .models import Employee, Employer, Event, Material, MaterialRequest, MaterialRequestSignature, Project, OrganizationUnit, Service, ServiceRequest, ServiceRequestSignature
from utility.persian import PersianCalendar

class ProjectRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Project.objects
        self.me=ProfileRepo(user=self.user).me

    # def edit_project_timing(self,project_id,percentage_completed,start_date,end_date):
    def edit_project_timing(self,*args, **kwargs):
        project=self.project(*args, **kwargs)
        if project is not None:
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'start_date' in kwargs:
                project.start_date=kwargs['start_date']
            if 'end_date' in kwargs:
                project.end_date=kwargs['end_date']
            project.save()
            return project



    def add_organization_unit(self,*args, **kwargs):
        project=self.project(*args, **kwargs)
        organization_unit=OrganizationUnitRepo(user=self.user).organization_unit(*args, **kwargs)
        if organization_unit in project.organization_units.all():
            return None
        if project is not None and organization_unit is not None:
            project.organization_units.add(organization_unit)
            # project.save()
            # print(organization_unit)
            # print(10*"#35366647535")
            return organization_unit
             

    def project(self, *args, **kwargs):
        if 'project_id' in kwargs:
            pk=kwargs['project_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_project(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_project"):
            return None
        new_project = Project()

        if 'title' in kwargs:
            new_project.title = kwargs['title']

        if 'parent_id' in kwargs and kwargs['parent_id']>0:
            new_project.parent_id = kwargs['parent_id']

        new_project.creator=self.me
        new_project.save()
        return new_project


class OrganizationUnitRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = OrganizationUnit.objects

    def organization_unit(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'new_organization_id' in kwargs:
            return self.objects.filter(pk=kwargs['new_organization_id']).first()
        if 'organization_unit_id' in kwargs:
            return self.objects.filter(pk=kwargs['organization_unit_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_organization_unit(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_organizationunit"):
            return None
        new_organization = OrganizationUnit()

        if 'title' in kwargs:
            new_organization.title = kwargs['title']

        if 'employer_id' in kwargs and kwargs['employer_id'] is not None:
            new_organization.employer_id = kwargs['employer_id']

        if 'parent_id' in kwargs and kwargs['parent_id']==0:
            employer=Employer(title=kwargs['title'])
            employer.save()
            new_organization.employer = employer
        if 'parent_id' in kwargs and kwargs['parent_id'] is not None and kwargs['parent_id']>0:
            parent_organization =OrganizationUnit.objects.filter(pk=kwargs['parent_id']).first()
            if parent_organization is not None:
                new_organization.employer=parent_organization.employer
                new_organization.parent=parent_organization
        elif 'employer_title' in kwargs:
            pass
            

        new_organization.save()
        return new_organization

    def add_employee(self,*args, **kwargs):
        profile=ProfileRepo(user=self.request.user).profile(*args, **kwargs)
        if profile is None:
            from authentication.models import Profile
            profile=Profile()
            if 'first_name' in kwargs and 'last_name' in kwargs and 'username' in kwargs and 'password' in kwargs:
                from django.contrib.auth.models import User
                user=User.objects.create(first_name=kwargs['first_name'],last_name=kwargs['last_name'],username=kwargs['username'],password=kwargs['password'])
                user.save()
                user.set_password(kwargs['password'])
                user.save()
                profile=ProfileRepo(user=self.user).objects.filter(user=user).first()
                if profile is None:
                    return None
        organization_unit=OrganizationUnitRepo(request=self.request).organization_unit(*args, **kwargs)
        if profile is not None and organization_unit is not None:
            emp=Employee.objects.filter(profile=profile).filter(organization_unit=organization_unit).first()
            if emp is None:
                emp=Employee(profile=profile,organization_unit=organization_unit)
                emp.save()
                return emp
            


class EmployeeRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Employee.objects

    def employee(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'employee_id' in kwargs:
            return self.objects.filter(pk=kwargs['employee_id']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_employee(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_employee"):
            return None
        new_employee = Employee()

        if 'profile_id' in kwargs:
            new_employee.profile_id = kwargs['profile_id']

        if 'organization_unit_id' in kwargs:
            new_employee.organization_unit_id = kwargs['organization_unit_id']

        new_employee.save()
        return new_employee


class EmployerRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Employer.objects

    def employer(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'employer_id' in kwargs:
            return self.objects.filter(pk=kwargs['employee_id']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])

        return objects.all()

    def add_employer(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_employer"):
            return None
        new_employer = Employer()

        if 'title' in kwargs:
            new_employer.title = kwargs['title']
        if 'pre_title' in kwargs:
            new_employer.pre_title = kwargs['pre_title']

        new_employer.save()
        return new_employer


class ServiceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Service.objects

    def service(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'service_id' in kwargs:
            return self.objects.filter(pk=kwargs['service_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def service_request(self, *args, **kwargs):
        objects = ServiceRequest.objects
        if 'pk' in kwargs:
            return objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return objects.filter(pk=kwargs['id']).first()
        if 'service_request_id' in kwargs:
            return objects.filter(pk=kwargs['service_request_id']).first()
        if 'title' in kwargs:
            return objects.filter(pk=kwargs['title']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def add_signature(self,service_request_id,status,description=None):
        if self.user.has_perm(APP_NAME+".add_servicerequestsignature"):
            signature=ServiceRequestSignature()
            signature.description=description
            signature.service_request_id=service_request_id
            signature.status=status
            signature.profile=ProfileRepo(self.user).me
            signature.save()
            return signature


                   
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_service_request(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_servicerequest"):
            return None
        new_service_request = ServiceRequest(status=RequestStatusEnum.REQUESTED)
        if 'project_id' in kwargs:
            new_service_request.project_id = kwargs['project_id']
        if 'service_id' in kwargs:
            new_service_request.service_id = kwargs['service_id']
        if 'quantity' in kwargs:
            new_service_request.quantity = kwargs['quantity']
        if 'unit_name' in kwargs:
            new_service_request.unit_name = kwargs['unit_name']
        if 'unit_price' in kwargs:
            new_service_request.unit_price = kwargs['unit_price']
        if 'description' in kwargs:
            new_service_request.description = kwargs['description']
        if 'status' in kwargs:
            new_service_request.status = kwargs['status']
        if 'status' in kwargs:
            new_service_request.status = kwargs['status']
        if 'service_title' in kwargs:
            service=Service.objects.filter(title=kwargs['service_title']).first()
            if service is None:
                service=Service(title=kwargs['service_title'],unit_price=kwargs['unit_price'],unit_name=kwargs['unit_name'])
                service.save()            
            print(service)
            print(100*"#2455346")
            new_service_request.service_id=service.id
        profile = ProfileRepo(user=self.user).me
        new_service_request.profile = profile
        if new_service_request.quantity > 0 and new_service_request.unit_price > 0:
            new_service_request.save()
            new_service_request.service.unit_price = new_service_request.unit_price
            new_service_request.service.unit_name = new_service_request.unit_name
            new_service_request.service.save()
            service_request_signature=ServiceRequestSignature(profile=profile,service_request=new_service_request,status=SignatureStatusEnum.REQUESTED)
            service_request_signature.save()
            return new_service_request

    def add_service(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_service"):
            return None
        new_service = Service(unit_name=UnitNameEnum.SERVICE,unit_price=0)

       
        if 'title' in kwargs:
            new_service.title = kwargs['title']
        if 'parent_id' in kwargs:
            new_service.parent_id = kwargs['parent_id']
        new_service.save()
        return new_service


class EventRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Event.objects

    def event(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'event_id' in kwargs:
            return self.objects.filter(pk=kwargs['event_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
    def add_event(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_event"):
            return None
        if 'event_datetime' in kwargs:
            event_datetime=kwargs['event_datetime']
        else:
            from django.utils import timezone
            event_datetime=timezone.now()
        new_event=Event(adder=ProfileRepo(self.user).me,event_datetime=event_datetime)
        if 'project_id' in kwargs:
            new_event.project_related_id = kwargs['project_id']
        if 'title' in kwargs:
            new_event.title = kwargs['title']
        if 'event_datetime' in kwargs:
            event_datetime = kwargs['event_datetime']

            event_datetime=PersianCalendar().to_gregorian(event_datetime)
            new_event.event_datetime=event_datetime
            
        new_event.save()
        return new_event


class MaterialRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Material.objects

    def material(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'material_id' in kwargs:
            return self.objects.filter(pk=kwargs['material_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def material_request(self, *args, **kwargs):
        objects = MaterialRequest.objects
        if 'pk' in kwargs:
            return objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return objects.filter(pk=kwargs['id']).first()
        if 'material_request_id' in kwargs:
            return objects.filter(pk=kwargs['material_request_id']).first()
        if 'title' in kwargs:
            return objects.filter(pk=kwargs['title']).first()

    def get(self, *args, **kwargs):
        return self.organization_unit(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

    def add_material_request(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_materialrequest"):
            return None
        new_material_request = MaterialRequest(status=RequestStatusEnum.REQUESTED)
        if 'project_id' in kwargs:
            new_material_request.project_id = kwargs['project_id']
        if 'material_id' in kwargs:
            new_material_request.material_id = kwargs['material_id']
        if 'quantity' in kwargs:
            new_material_request.quantity = kwargs['quantity']
        if 'unit_name' in kwargs:
            new_material_request.unit_name = kwargs['unit_name']
        if 'unit_price' in kwargs:
            new_material_request.unit_price = kwargs['unit_price']
        if 'description' in kwargs:
            new_material_request.description = kwargs['description']
        if 'status' in kwargs:
            new_material_request.status = kwargs['status']
        if 'status' in kwargs:
            new_material_request.status = kwargs['status']
        profile = ProfileRepo(user=self.user).me
        new_material_request.profile = profile
        if new_material_request.quantity > 0 and new_material_request.unit_price > 0:
            new_material_request.save()
            new_material_request.material.unit_price = new_material_request.unit_price
            new_material_request.material.unit_name = new_material_request.unit_name
            new_material_request.material.save()
            material_request_signature=MaterialRequestSignature(profile=profile,material_request=new_material_request,status=SignatureStatusEnum.REQUESTED)
            material_request_signature.save()
            return new_material_request

    def add_material(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_material"):
            return None
        new_material = Material(image_main_origin="core/images/Page/Image/material.png")

        if 'parent_id' in kwargs and kwargs['parent_id']>0:
            new_material.parent_id = kwargs['parent_id']

        if 'title' in kwargs:
            new_material.title = kwargs['title']
        if 'short_description' in kwargs:
            new_material.short_description = kwargs['short_description']
        else:
            new_material.short_description =new_material.full_title

        new_material.save()
        return new_material
    
    def add_signature(self,material_request_id,status,description=None):
        if self.user.has_perm(APP_NAME+".add_materialrequestsignature"):
            signature=MaterialRequestSignature()
            signature.description=description
            signature.material_request_id=material_request_id
            signature.status=status
            signature.profile=ProfileRepo(self.user).me
            signature.save()
            return signature

