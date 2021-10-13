from django.db.models.aggregates import Avg
from django.utils import timezone
from projectmanager.enums import ProjectStatusEnum, RequestStatusEnum, SignatureStatusEnum, UnitNameEnum, WareHouseSheetDirectionEnum
from authentication.repo import ProfileRepo
from django.db.models import Q,Sum
from .apps import APP_NAME
from .models import Location,Employee, Employer, Event, Material, MaterialRequest, Project, OrganizationUnit, Location, ProjectManagerPage, RequestSignature, Service, ServiceRequest, WareHouse, WareHouseExportSheet, WareHouseImportSheet, WareHouseMaterial, WareHouseSheet, WareHouseSheetLine
from core.repo import ParameterRepo
from .enums import ParametersEnum

def show_archives(request):
        parameter_repo = ParameterRepo(request=request,app_name=APP_NAME)
        show_archives=parameter_repo.parameter(ParametersEnum.SHOW_ARCHIVES).boolesan_value
        return show_archives
class ProjectRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Project.objects.filter(id=0)
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user is None:
            self.objects=Project.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_project"):
            self.objects = Project.objects.order_by('priority')
        elif self.profile is not None:
            employees=Employee.objects.filter(profile=self.profile)
            lisst=[]
            for employee in employees:
                for proj in employee.my_projects():
                    lisst.append(proj.id)
            self.objects=Project.objects.filter(id__in=lisst)
        
        if_show_archives=show_archives(request=self.request)
        self.objects=self.objects.all()
        if not if_show_archives:
            self.objects=self.objects.filter(archive=False)
    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        project_id=0
        if 'project_id' in kwargs:
            project_id=kwargs['project_id']
        location=LocationRepo(request=self.request,user=self.user).add_location(*args, **kwargs)
        project=self.project(project_id=project_id)
        project.locations.add(location)
        project.save()
        return location

    def copy_project_request(self,*args, **kwargs):
        destination_project_id=kwargs['destination_project_id'] if 'destination_project_id' in kwargs else None
        source_project_id=kwargs['source_project_id'] if 'source_project_id' in kwargs else None
        request_type=kwargs['request_type'] if 'request_type' in kwargs else None
        destination_project=self.project(pk=destination_project_id)
        source_project=self.project(pk=source_project_id)
        if destination_project is None or source_project is None:
            return
        if request_type=="service":
            for source_service_request in ServiceRequest.objects.filter(project=source_project):
                
                ServiceRequestRepo(request=self.request).add_service_request(
                    service_id=source_service_request.service_id,
                    project_id=destination_project_id,
                    quantity=source_service_request.quantity,
                    handler_id=source_service_request.handler_id,
                    employee_id=source_service_request.handler_id,
                    unit_name=source_service_request.unit_name,
                    unit_price=source_service_request.unit_price,
                    description=source_service_request.description
                )

        if request_type=="material":
            for source_material_request in MaterialRequest.objects.filter(project=source_project):
                MaterialRequestRepo(request=self.request).add_material_request(
                    material_id=source_material_request.material_id,
                    project_id=destination_project_id,
                    quantity=source_material_request.quantity,
                    handler_id=source_material_request.handler_id,
                    unit_name=source_material_request.unit_name,
                    unit_price=source_material_request.unit_price,
                    description=source_material_request.description
                )
        return destination_project    

    # def edit_project_timing(self,project_id,percentage_completed,start_date,end_date):
    def edit_project(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_project"):
            return None
        project=self.project(*args, **kwargs)
        if project is not None:
            if 'percentage_completed' in kwargs:
                project.percentage_completed=kwargs['percentage_completed']
            if 'start_date' in kwargs:
                project.start_date=kwargs['start_date']
            if 'end_date' in kwargs:
                project.end_date=kwargs['end_date']
            if 'status' in kwargs:
                project.status=kwargs['status']
            if 'contractor_id' in kwargs:
                project.contractor_id=kwargs['contractor_id']
            if 'employer_id' in kwargs:
                project.employer_id=kwargs['employer_id']
            if 'title' in kwargs:
                project.title=kwargs['title']
            if 'weight' in kwargs:
                project.weight=kwargs['weight']
                pass
            if 'archive' in kwargs:
                project.archive=kwargs['archive']
            project.save()
            return project



    def add_organization_unit(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_project"):
            return None
        project=self.project(*args, **kwargs)
        organization_unit=OrganizationUnitRepo(user=self.user).organization_unit(*args, **kwargs)
        if organization_unit in project.organization_units.all():
            return None
        if project is not None and organization_unit is not None:
            project.organization_units.add(organization_unit)
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

        new_project.creator=self.profile
        now=timezone.now()
        new_project.start_date=now
        new_project.end_date=now
        new_project.status=ProjectStatusEnum.INITIAL
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
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user is None:
            self.objects=OrganizationUnit.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_organizationunit"):
            self.objects = OrganizationUnit.objects
        elif self.profile is not None:
            employees=self.profile.employee_set.all()
            ids=[]
            for employee in employees:
                ids.append(employee.organization_unit.id)
            self.objects=OrganizationUnit.objects.filter(id__in=ids)
        else:
            self.objects=OrganizationUnit.objects.filter(id=0)

    def organization_unit(self, *args, **kwargs):
        pk=0
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
        if 'is_ware_house' in kwargs and kwargs['is_ware_house']==True:
            new_organization = WareHouse()
        else:
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
        if not self.user.has_perm(APP_NAME+".add_employee"):
            return None
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
            

class WareHouseSheetRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouseSheet.objects
        self.me_employee=EmployeeRepo(request=self.request).me

    def add_material_request_to_ware_house_sheet(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_warehousesheetline"):
            return
        material_request=None

        ware_house_export_sheet_id=kwargs['ware_house_export_sheet_id'] if 'ware_house_export_sheet_id' in kwargs else None
        ware_house_import_sheet_id=kwargs['ware_house_import_sheet_id'] if 'ware_house_import_sheet_id' in kwargs else None
        material_request_id=kwargs['material_request_id'] if 'material_request_id' in kwargs else None
        ware_house_id=kwargs['ware_house_id'] if 'ware_house_id' in kwargs else None
        
        material_request=MaterialRequestRepo(request=self.request).material_request(material_request_id=material_request_id)
        ware_house=WareHouseRepo(request=self.request).ware_house(ware_house_id=ware_house_id)
        
        if material_request is None:
            return None
        

        # create new sheet line
        sheet_line=WareHouseSheetLine()
        sheet_line.material=material_request.material
        sheet_line.quantity=material_request.quantity
        sheet_line.unit_name=material_request.unit_name
        sheet_line.unit_price=material_request.unit_price
        sheet_line.description=f"""مربوط به پروژه  <a href="{material_request.project.get_absolute_url()}">{material_request.project.title}</a> """
            
        # create new ware_house_export_sheet
        if ware_house_export_sheet_id is not None and ware_house_export_sheet_id==0  and ware_house is not None:
            sheet=WareHouseExportSheet()
            sheet.description=f"""مربوط به پروژه  <a href="{material_request.project.get_absolute_url()}">{material_request.project.title}</a> """
            sheet.date_exported=timezone.now()
            sheet.ware_house=ware_house
            sheet.save()
        # create new ware_house_import_sheet
        if ware_house_import_sheet_id is not None and ware_house_import_sheet_id==0  and ware_house is not None:
            sheet=WareHouseImportSheet()
            sheet.description=f"""مربوط به پروژه  <a href="{material_request.project.get_absolute_url()}">{material_request.project.title}</a> """
            sheet.date_imported=timezone.now()
            sheet.ware_house=ware_house
            sheet.save()



        # ADD to existing export Sheet
        if ware_house_export_sheet_id is not None and ware_house_export_sheet_id>0:  
            sheet=WareHouseExportSheetRepo(request=self.request).ware_house_export_sheet(pk=ware_house_export_sheet_id)          
            sheet_line.ware_house_sheet_id=ware_house_export_sheet_id

        # ADD to existing import Sheet
        if ware_house_import_sheet_id is not None and ware_house_import_sheet_id>0:
            sheet=WareHouseImportSheetRepo(request=self.request).ware_house_import_sheet(pk=ware_house_import_sheet_id)
            sheet_line.ware_house_sheet_id=ware_house_import_sheet_id


        
        
        sheet.creator=self.me_employee
        sheet_line.ware_house_sheet=sheet


        if 'date_exported' in kwargs:
            sheet_line.ware_house_sheet.date_exported=kwargs['date_exported']
        if 'date_imported' in kwargs:
            sheet_line.ware_house_sheet.date_imported=kwargs['date_imported']
        if 'employee_id' in kwargs:
            sheet_line.employee_id=kwargs['employee_id']
        if 'description' in kwargs:
            sheet_line.description=kwargs['description']

        sheet.save()
        sheet_line.save()
        material_request.ware_house_sheet=sheet
        material_request.save()
        return sheet

    
    def ware_house_sheet(self, *args, **kwargs):
        objects=WareHouseSheet.objects
        pk=0
        if 'ware_house_sheet_id' in kwargs:
            return objects.filter(pk=kwargs['ware_house_sheet_id']).first()
        if 'pk' in kwargs:
            return objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return objects.filter(pk=kwargs['id']).first()
    

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'ware_house' in kwargs:
            objects = objects.filter(ware_house=kwargs['ware_house'])
        if 'ware_house_id' in kwargs:
            objects = objects.filter(ware_house_id=kwargs['ware_house_id'])
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects


class WareHouseMaterialRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouseMaterial.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'ware_house' in kwargs:
            objects=objects.filter(ware_house=kwargs['ware_house'])
        if 'ware_house_id' in kwargs:
            objects=objects.filter(ware_house_id=kwargs['ware_house_id'])
        if 'material' in kwargs:
            objects=objects.filter(material=kwargs['material'])
        if 'material_id' in kwargs:
            objects=objects.filter(material_id=kwargs['material_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            q=Q(pk=0)
            q=q|Q(material__title__contains=search_for)
            q=q|Q(code__contains=search_for)
            q=q|Q(description__contains=search_for)
            objects=objects.filter(q)
        return objects
        


    def ware_house_material(self, *args, **kwargs):
        pk=0
        if 'ware_house_material_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_material_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()


class WareHouseRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouse.objects
    def ware_house(self, *args, **kwargs):
        pk=0
        if 'ware_house_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    def ware_house_materials(self,*args, **kwargs):
        ware_house_materials=[]
        return []
        if 'ware_house_id' in kwargs:
            ware_house_id=kwargs['ware_house_id']
            ware_house=WareHouse.objects.filter(ok=ware_house_id).first()
            if ware_house is None:
                return ware_house_materials
        if 'ware_house' in kwargs:
            ware_house=kwargs['ware_house']
        for ware_house_sheet in ware_house.warehousesheet_set.filter(direction=WareHouseSheetDirectionEnum.EXPORT):
            for ware_house_material in ware_house_sheet.material_requests.filter(status=RequestStatusEnum.DELIVERED).values('material_id','unit_name').annotate(total_quantities=Sum('quantity')).annotate(average_unit_price=Avg('unit_price')):
                material=MaterialRepo(request=self.request).material(pk=ware_house_material['material_id'])
                ware_house_materials.append({
                    'material':material,
                    'unit_name':ware_house_material['unit_name'],
                    'total_quantities':ware_house_material['total_quantities'],
                    'direction':WareHouseSheetDirectionEnum.EXPORT,
                    'average_unit_price':ware_house_material['average_unit_price'],
                    'direction_color':'danger',
                    'total_price':ware_house_material['average_unit_price']*ware_house_material['total_quantities'],
                })
        for ware_house_sheet in ware_house.warehousesheet_set.filter(direction=WareHouseSheetDirectionEnum.IMPORT):
            for ware_house_material in ware_house_sheet.material_requests.filter(status=RequestStatusEnum.AVAILABLE_IN_STORE).values('material_id','unit_name').annotate(total_quantities=Sum('quantity')).annotate(average_unit_price=Avg('unit_price')):
                material=MaterialRepo(request=self.request).material(pk=ware_house_material['material_id'])
                ware_house_materials.append({
                    'material':material,
                    'unit_name':ware_house_material['unit_name'],
                    'total_quantities':ware_house_material['total_quantities'],
                    'direction':WareHouseSheetDirectionEnum.IMPORT,
                    'average_unit_price':ware_house_material['average_unit_price'],
                    'direction_color':'success',
                    'total_price':ware_house_material['average_unit_price']*ware_house_material['total_quantities'],
                })

        
        return ware_house_materials

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects


class WareHouseExportSheetRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouseExportSheet.objects
    def ware_house_export_sheet(self, *args, **kwargs):
        pk=0
        if 'ware_house_export_sheet_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_export_sheet_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

  
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects


class WareHouseImportSheetRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouseImportSheet.objects
    def ware_house_import_sheet(self, *args, **kwargs):
        pk=0
        if 'ware_house_export_sheet_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_export_sheet_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

  
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects


class WareHouseSheetLineRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouseSheetLine.objects
    def ware_house_sheet_line(self, *args, **kwargs):
        pk=0
        if 'ware_house_sheet_line_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_sheet_line_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'material' in kwargs:
            objects = objects.filter(material=kwargs['material'])
        if 'material_id' in kwargs:
            objects = objects.filter(material_id=kwargs['material_id'])
        if 'ware_house_id' in kwargs:
            objects = objects.filter(ware_house_sheet__ware_house_id=kwargs['ware_house_id'])
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects


class EmployeeRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(request=self.request).me
        if self.user is None:
            self.objects=Employee.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_employee"):
            self.objects = Employee.objects
        elif self.profile is not None:
            self.objects=Employee.objects.filter(id=0)
            self.me=Employee.objects.filter(profile=self.profile).first()
        else:
            self.objects=Employee.objects.filter(id=0)

        self.me=Employee.objects.filter(profile=self.profile).first()
    
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
        
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user is None:
            self.objects=Employee.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_employer"):
            self.objects = Employer.objects
        elif self.profile is not None:
            self.objects=Employer.objects.filter(id=0)
        else:
            self.objects=Employer.objects.filter(id=0)

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
        self.me=ProfileRepo(user=self.user).me
        self.employee=EmployeeRepo(request=self.request).me

    def service(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'service_id' in kwargs:
            return self.objects.filter(pk=kwargs['service_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'for_home' in kwargs:
            objects = objects.filter(
                Q(for_home=kwargs['for_home']) | Q(parent=None))
        return objects.all()

  
    def add_service(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_service"):
            return None
        new_service = Service(unit_name=UnitNameEnum.SERVICE,unit_price=0)

       
        if 'title' in kwargs:
            new_service.title = kwargs['title']
        if 'parent_id' in kwargs and kwargs['parent_id']>0:
            
            new_service.parent_id = kwargs['parent_id']
        new_service.creator=self.me    
        new_service.save()
        return new_service


class ServiceRequestRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects = ServiceRequest.objects.order_by('-date_added')
        if_show_archives=show_archives(request=self.request)
        if not if_show_archives:
            self.objects = self.objects.filter(project__archive=False)
        self.me=ProfileRepo(user=self.user).me
        self.employee=EmployeeRepo(request=self.request).me

   
    def service_request(self, *args, **kwargs):
        objects = self.objects
        if 'pk' in kwargs:
            return objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return objects.filter(pk=kwargs['id']).first()
        if 'service_request_id' in kwargs:
            return objects.filter(pk=kwargs['service_request_id']).first()
        if 'title' in kwargs:
            return objects.filter(pk=kwargs['title']).first()

   
    def add_signature(self,*args, **kwargs):
        status=kwargs['status'] if 'status' in kwargs else SignatureStatusEnum.DEFAULT
        description=kwargs['description'] if 'description' in kwargs else ""
        service_request=self.service_request(*args, **kwargs)        
        me_employee=EmployeeRepo(request=self.request).me


        if service_request is None or  me_employee is None:
            return
        if self.user.has_perm(APP_NAME+".add_requestsignature"):
            pass
        elif service_request.project in me_employee.my_projects():
            pass
        else:
            return
        
        signature=RequestSignature()
        signature.description=description
        service_request.status=status
        service_request.save()

        signature.request=service_request
        signature.status=status
        signature.date_added=timezone.now()
        signature.employee=me_employee
        signature.save()

        return signature

    
    def service_requests(self,*args, **kwargs):
        objects=self.objects
        if 'project_id' in kwargs:
            objects=objects.filter(project_id=kwargs['project_id'])
        if 'service_id' in kwargs:
            objects=objects.filter(service_id=kwargs['service_id'])
        if 'employee_id' in kwargs:
            objects=objects.filter(handler_id=kwargs['employee_id'])
        return objects
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
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
        if 'employee_id' in kwargs:
            handler_id = kwargs['employee_id']
            employee_id = kwargs['employee_id']
        if 'handler_id' in kwargs:
            handler_id = kwargs['handler_id']
            if not employee_id==0:
                new_service_request.employee_id=employee_id
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
            new_service_request.service_id=service.id
        profile = ProfileRepo(user=self.user).me
        new_service_request.handler_id = handler_id
        new_service_request.creator=self.employee
        if new_service_request.quantity > 0 and new_service_request.unit_price > 0:
            new_service_request.save()
            new_service_request.service.unit_price = new_service_request.unit_price
            new_service_request.service.unit_name = new_service_request.unit_name
            new_service_request.service.save()
            service_request_signature=RequestSignature(employee=self.employee,request=new_service_request,status=SignatureStatusEnum.REQUESTED)
            service_request_signature.save()
            return new_service_request
 

class EventRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user is None:
            self.objects=Employee.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_event"):
            self.objects = Event.objects
        elif self.profile is not None:
            self.objects=Event.objects.filter(id=0)
        else:
            self.objects=Event.objects.filter(id=0)

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
        if 'start_datetime' in kwargs:
            start_datetime=kwargs['start_datetime']
        if 'end_datetime' in kwargs:
            end_datetime=kwargs['end_datetime']
        else:
            from django.utils import timezone
            event_datetime=timezone.now()
        new_event=Event(creator=ProfileRepo(user=self.user).me,event_datetime=event_datetime)
        if 'project_id' in kwargs:
            new_event.project_related_id = kwargs['project_id']
        if 'title' in kwargs:
            new_event.title = kwargs['title']
        if 'event_datetime' in kwargs:
            event_datetime = kwargs['event_datetime']

        # event_datetime=PersianCalendar().to_gregorian(event_datetime)
        new_event.event_datetime=event_datetime
        new_event.end_datetime=end_datetime
        new_event.start_datetime=start_datetime
        new_event.creator=self.profile
        new_event.save()
        return new_event

    def search(self,search_for):
        objects = self.objects.filter(title__contains=search_for)
        return objects


class MaterialRequestRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
            
        self.objects = MaterialRequest.objects.order_by('-date_added')
        if_show_archives=show_archives(request=self.request)
        if not if_show_archives:
            self.objects = self.objects.filter(project__archive=False)
        self.employee=EmployeeRepo(request=self.request).me

    def material_request(self, *args, **kwargs):
        objects = self.objects
        if 'pk' in kwargs:
            return objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return objects.filter(pk=kwargs['id']).first()
        if 'material_request_id' in kwargs:
            return objects.filter(pk=kwargs['material_request_id']).first()
        if 'title' in kwargs:
            return objects.filter(pk=kwargs['title']).first()

    def list(self, *args, **kwargs):
        objects=self.objects
        if 'project_id' in kwargs:
            objects=objects.filter(project_id=kwargs['project_id'])
        if 'material_id' in kwargs:
            objects=objects.filter(material_id=kwargs['material_id'])
        if 'employee_id' in kwargs:
            objects=objects.filter(handler_id=kwargs['employee_id'])
        return objects

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
        if 'employee_id' in kwargs:
            new_material_request.handler_id = kwargs['employee_id']
        if 'handler_id' in kwargs:
            new_material_request.handler_id = kwargs['handler_id']
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
        new_material_request.creator = self.employee
        if new_material_request.quantity > 0 and new_material_request.unit_price > 0:
            new_material_request.save()
            new_material_request.material.unit_price = new_material_request.unit_price
            new_material_request.material.unit_name = new_material_request.unit_name
            new_material_request.material.save()
            material_request_signature=RequestSignature(employee=self.employee,request=new_material_request,status=SignatureStatusEnum.REQUESTED)
            material_request_signature.save()
            return new_material_request

    def add_signature(self,material_request_id,status,description=None):
        if self.user.has_perm(APP_NAME+".add_materialrequestsignature"):
            signature=RequestSignature()
            signature.description=description
            signature.request_id=material_request_id
            material_request=self.material_request(material_request_id=material_request_id)
            if material_request is not None:
                material_request.status=status
                material_request.save()
            signature.status=status
            signature.date_added=timezone.now()
            signature.employee=EmployeeRepo(request=self.request).me
            signature.save()
            return signature

    def material_requests(self,*args, **kwargs):
        return self.list(*args, **kwargs)


class LocationRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user is None:
            self.objects=Employee.objects.filter(id=0)
        elif self.user.has_perm(APP_NAME+".view_location"):
            self.objects = Location.objects
        elif self.profile is not None:
            self.objects=Event.objects.filter(id=0)
        else:
            self.objects=Event.objects.filter(id=0)
    def pages(self,location):
        pages=[]
        for project in Project.objects.all():
            if location in project.locations.all():
                pages.append(project)
        for event in Event.objects.all():
            if location in event.locations.all():
                pages.append(event)
        return pages
    def location(self, *args, **kwargs):
        if 'location_id' in kwargs:
            return self.objects.filter(pk=kwargs['location_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
    def add_existing_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location_id=0
        if 'location_id' in kwargs:
            location_id=kwargs['location_id']
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        location=self.location(location_id=location_id)
        page=ProjectManagerPage.objects.filter(pk=page_id).first()
        if page is not None:
            if page.class_name=='project':
                Project.objects.filter(pk=page_id).first().locations.add(location)
            if page.class_name=='event':
                Event.objects.filter(pk=page_id).first().locations.add(location)

        return location

    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location1=""
        title=""
        if 'location' in kwargs:
            location1=kwargs['location']
        if 'title' in kwargs:
            title=kwargs['title']
        location=Location()
        location.title=title
        location.creator=self.profile
        location.location=location1
        location.save()
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
            page=ProjectManagerPage.objects.filter(pk=page_id).first()
            if page is not None:
                if page.class_name=='project':
                    Project.objects.filter(pk=page_id).first().locations.add(location)
                if page.class_name=='event':
                    Event.objects.filter(pk=page_id).first().locations.add(location)

        return location
    def search(self,search_for):
        objects = self.objects.filter(title__contains=search_for)
        return objects
    def list(self,*args, **kwargs):
        objects = self.objects.order_by('title')
        return objects


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
        self.employee=EmployeeRepo(request=self.request).me

    def material(self, *args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'material_id' in kwargs:
            return self.objects.filter(pk=kwargs['material_id']).first()
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

    def add_material(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_material"):
            return None
        new_material = Material()

        if 'parent_id' in kwargs and kwargs['parent_id']>0:
            new_material.parent_id = kwargs['parent_id']

        if 'title' in kwargs:
            new_material.title = kwargs['title']
        if 'short_description' in kwargs:
            new_material.short_description = kwargs['short_description']
        else:
            new_material.short_description =f'<p>{new_material.full_title}</p>'

        new_material.save()
        return new_material
    
    def add_signature(self,material_request_id,status,description=None):
        if self.user.has_perm(APP_NAME+".add_materialrequestsignature"):
            signature=RequestSignature()
            signature.description=description
            signature.request_id=material_request_id
            material_request=self.material_request(material_request_id=material_request_id)
            if material_request is not None:
                material_request.status=status
                material_request.save()
            signature.status=status
            signature.date_added=timezone.now()
            signature.employee=EmployeeRepo(request=self.request).me
            signature.save()
            return signature
