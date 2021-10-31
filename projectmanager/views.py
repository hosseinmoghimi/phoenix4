import json

from django.http.response import Http404

from .apps import APP_NAME
from .forms import *
from .repo import EmployeeRepo, EmployerRepo, EventRepo, LocationRepo, MaterialRepo, MaterialRequestRepo, OrganizationUnitRepo, ProjectRepo, ServiceRepo, ServiceRequestRepo, WareHouseMaterialRepo, WareHouseRepo, WareHouseSheetLineRepo, WareHouseSheetRepo
from .serializers import EmployeeSerializer, EmployeeSerializer2, EmployerSerializer, EventSerializerForChart, MaterialRequestSerializer, MaterialSerializer, OrganizationUnitSerializer, ProjectSerializer, ProjectSerializerForGuantt, ServiceRequestSerializer, ServiceSerializer, WareHouseSheetLineSerializer, WareHouseSheetSerializer
from .utils import AdminUtility
from authentication.repo import ProfileRepo
from authentication.views import ProfileContext
from authentication.serializers import ProfileSerializer
from core.constants import CURRENCY
from core.enums import AppNameEnum, ParametersEnum
from core.repo import ParameterRepo, PictureRepo, TagRepo
from core.serializers import BasicPageSerializer
from core.views import DefaultContext, MessageView, PageContext
from django.views import View
from django.shortcuts import redirect, render
from projectmanager.enums import ProjectStatusEnum, RequestStatusEnum, SignatureStatusEnum, UnitNameEnum
from utility.persian import PersianCalendar
from web.repo import CarouselRepo
TEMPLATE_ROOT = APP_NAME+"/"


def getContext(request):
    context = DefaultContext(request=request, app_name=APP_NAME)
    context['layout_parent']="material-dashboard-5-rtl/layout.html"
    context['layout_parent']="material-kit-pro/layout.html"
    context['layout_parent']="phoenix/layout.html"
    context["layout"] = TEMPLATE_ROOT+"layout.html"
    context['help_url']=reverse("help:app",kwargs={"app_name":APP_NAME})
    me_employee=EmployeeRepo(request=request).me
    context["me_employee"] =me_employee
    context["admin_utility"] = AdminUtility(request=request)
    context['search_action'] = reverse(APP_NAME+":search")
    context['search_form'] = SearchForm()
    parameter_repo = ParameterRepo(app_name=APP_NAME)
    context['app'] = {
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(ParametersEnum.TEL).value,
        'title': parameter_repo.get(ParametersEnum.TITLE).value,
    }
    return context


class LoactionViews(View):
    def location(self, request, *args, **kwargs):
        context = getContext(request)
        repo=LocationRepo(request=request)
        location=repo.location(*args, **kwargs)
        context['location']=location
        pages=repo.pages(location)
        context['pages']=pages
        return render(request, TEMPLATE_ROOT+"location.html", context)


class BasicViews(View):
    def search(self, request, *args, **kwargs):
        context = getContext(request)
        log = 1
        if request.method == 'POST':
            log += 1
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                log += 1
                search_for = search_form.cleaned_data['search_for']
                context['search_for'] = search_for
                context['materials'] = MaterialRepo(
                    request=request).list(search_for=search_for)
                context['services'] = ServiceRepo(
                    request=request).list(search_for=search_for)
                context['employers'] = EmployerRepo(
                    request=request).list(search_for=search_for)
                context['projects'] = ProjectRepo(
                    request=request).list(search_for=search_for)
                context['tags'] = TagRepo(
                    request=request).list(search_for=search_for)
                context['events'] = EventRepo(
                    request=request).search(search_for=search_for)
                context['organization_units'] = OrganizationUnitRepo(
                    request=request).list(search_for=search_for)
                context['log'] = log
                return render(request, TEMPLATE_ROOT+"search.html", context)
        return BasicViews().home(request=request)

    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['parent_id'] = 0
        picture_repo=PictureRepo(request=request,app_name=APP_NAME)
        carousel_repo=CarouselRepo(request=request,app_name=APP_NAME)
        splash=picture_repo.get(name="index.splash")
        context['splash']=splash
        context['locations']=LocationRepo(request=request).list()
        carousels=carousel_repo.list()
        if len(carousels)>0:
            context['carousels']=carousels
        if request.user.has_perm(APP_NAME+".add_service"):
            context['add_service_form'] = AddServiceForm()
        if request.user.has_perm(APP_NAME+".add_organizationunit"):
            context['add_organization_unit_form'] = AddOrganizationUnitForm()
        if request.user.has_perm(APP_NAME+".add_employer"):
            context['add_employer_form'] = AddEmployerForm()
        if request.user.has_perm(APP_NAME+".add_material"):
            context['add_material_form'] = AddMaterialForm()
        if request.user.has_perm(APP_NAME+".add_project"):
            context['add_project_form'] = AddProjectForm()
        if request.user.has_perm(APP_NAME+".add_location"):
            context['add_location_form'] = AddLocationForm()
        context['services'] = ServiceRepo(request=request).list(for_home=True)
        context['projects'] = ProjectRepo(request=request).list(for_home=True)
        context['materials'] = MaterialRepo(
            request=request).list(for_home=True)
        context['employers'] = EmployerRepo(
            request=request).list(for_home=True)
        organization_units = OrganizationUnitRepo(
            request=request).list(for_home=True)
        context['organization_units'] = organization_units
        context['organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['all_organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)

        return render(request, TEMPLATE_ROOT+"index.html", context)


class ProjectViews(View):
    def copy_project_request(self,request,*args, **kwargs):
        if 'destination_project_id' in kwargs:
            destination_project_id=kwargs['destination_project_id']
            if request.method=='POST':
                copy_project_request_form=CopyProjectRequestForm(request.POST)
                if copy_project_request_form.is_valid():
                    source_project_id=copy_project_request_form.cleaned_data['source_project_id']
                    request_type=copy_project_request_form.cleaned_data['request_type']
                    project=ProjectRepo(request=request).copy_project_request(
                        destination_project_id=destination_project_id,
                        source_project_id=source_project_id,
                        request_type=request_type
                        )
                    if project is not None:
                        return redirect(project.get_absolute_url())
        raise Http404
    def projects_chart(self, request, *args, **kwargs):
        context = getContext(request)
        if 'pk' in kwargs and kwargs['pk']>0:
            pk=kwargs['pk']
        else:
            pk=0

        project=(ProjectRepo(request=request).project(pk=pk))
        pages=project.all_childs()
        # pages_s = BasicPageSerializer(pages, many=True).data
        
        pages_s=[]
        # pages_s = BasicPageSerializer(pages, many=True).data
        from utility.currency import to_price
        pages2=[project]
        
        for page in pages:
            pages2.append(page)
        
        for page in pages2:
            pages_s.append({
                'title':f"""{page.title}""",
                'parent_id':page.parent_id,
                'parent':page.parent_id,
                'get_absolute_url':page.get_absolute_url(),
                'id':page.id,
                'sub_title':f"""<div class="small"> {page.percentage_completed}% <span class="badge badge-{page.get_status_color()}">{page.status}</span></div><div class="small">{to_price(page.sum_total())}</div>""",

            })
        # page=project
        # pages_s.append({
        #     'title':f"""{page.title}""",
        #     'parent_id':page.parent_id,
        #     'parent':page.parent_id,
        #     'get_absolute_url':page.get_absolute_url(),
        #     'id':page.id,
        #     'sub_title':f"""<div class="small"> {page.percentage_completed}% <span class="badge badge-{page.get_status_color()}">{page.status}</span></div><div class="small">{to_price(page.sum_total())}</div>""",

        # })
        context['pages_s'] = json.dumps(pages_s)

        return render(request, "phoenix/pages-chart.html", context)

    

    def guantt(self, request, *args, **kwargs):
        context = getContext(request=request)
        
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context['project'] = project
        context['projects_s'] = json.dumps(
            ProjectSerializerForGuantt(project.sub_projects().all(), many=True).data)

        return render(request, TEMPLATE_ROOT+"guantt.html", context)

    
    def project_materials_order(self, request, *args, **kwargs):
        context = getContext(request)
        TAX_PERCENT = 0
        project = ProjectRepo(request=request).project(*args, **kwargs)
        order_lines = []
        lines_total = 0
        for material_request in MaterialRequestRepo(request=request).material_requests(project_id=project.id):
            quantity = material_request.quantity
            unit_name = material_request.unit_name
            unit_price = material_request.unit_price
            lines_total += (quantity*unit_price)
            order_lines.append({
                'quantity': quantity,
                'unit_name': unit_name,
                'unit_price': unit_price,
                'line_total': quantity*unit_price,
                'product': material_request.material,
            })

        tax = int(TAX_PERCENT*(lines_total)/100)
        ship_fee = 0
        
        descriptions = [
            f"واحد مبلغ ها {CURRENCY} می باشد.",
            f"""مربوط به پروژه  {project.full_title}     ({project.id})""",
            ]
            
        total_for_pay = tax+lines_total
        print_date = PersianCalendar().date
        order = {
            'customer': project.employer,
            'supplier': project.contractor,
            'tax': tax,
            'lines_total': lines_total,
            'ship_fee': ship_fee,
            'total_for_pay': total_for_pay,
            'print_date': print_date,
            'descriptions': descriptions,
        }
        context['order_lines'] = order_lines
        context['order'] = order
        context['project'] = project
        return render(request, TEMPLATE_ROOT+"order.html", context)

    def project_services_order(self, request, *args, **kwargs):
        context = getContext(request)
        TAX_PERCENT = 0
        project = ProjectRepo(request=request).project(*args, **kwargs)
        order_lines = []
        lines_total = 0
        for service_request in ServiceRequestRepo(request=request).service_requests(project_id=project.id):
            quantity = service_request.quantity
            unit_name = service_request.unit_name
            unit_price = service_request.unit_price
            lines_total += (quantity*unit_price)
            order_lines.append({
                'quantity': quantity,
                'unit_name': unit_name,
                'unit_price': unit_price,
                'line_total': quantity*unit_price,
                'product': service_request.service,
            })

        tax = int(TAX_PERCENT*(lines_total)/100)
        ship_fee = 0
        
        descriptions = [
            f"واحد مبلغ ها {CURRENCY} می باشد.",
            f"""مربوط به پروژه  {project.full_title}     ({project.id})""",
            ]
        total_for_pay = tax+lines_total
        print_date = PersianCalendar().date
        order = {
            'customer': project.employer,
            'supplier': project.contractor,
            'tax': tax,
            'lines_total': lines_total,
            'ship_fee': ship_fee,
            'total_for_pay': total_for_pay,
            'print_date': print_date,
            'descriptions': descriptions,
        }
        context['order'] = order
        context['order_lines'] = order_lines
        context['project'] = project
        return render(request, TEMPLATE_ROOT+"order.html", context)

    def project(self, request, *args, **kwargs):
        project = ProjectRepo(request=request).project(*args, **kwargs)

        if project is None:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین پروژه ای وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.response(request=request,app_name=APP_NAME,*args, **kwargs)
        page = project
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        employees=project.employees()
        context['employees']=employees
        context['locations']=project.locations.all()
        material_requests=MaterialRequestRepo(request=request).material_requests(project_id=project.id)
        service_requests=ServiceRequestRepo(request=request).service_requests(project_id=project.id)
        context['material_requests']=material_requests
        context['material_requests_s']=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        context['service_requests']=service_requests
        context['service_requests_s']=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        context['employees_s']=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['project'] = project
        context['all_locations']=LocationRepo(request=request).list().order_by('title')
        if request.user.has_perm(APP_NAME+'.change_project'):
            context['add_location_form'] = AddLocationForm()
            context['copy_project_request_form']=CopyProjectRequestForm()
            context['add_existing_location_form'] = AddExistingLocationForm()
            context['edit_project_form']=EditProjectForm()
            context['add_material_request_form'] = AddMaterialRequestForm()
            context['add_service_request_form'] = AddServiceRequestForm()
        if request.user.has_perm(APP_NAME+'.add_event'):
            context['add_event_form'] = AddEventForm()
        context['events'] = project.event_set.all().order_by('event_datetime')
        organization_units = project.organization_units.all()
        context['add_organization_unit_form'] = AddOrganizationUnitForm()
        context['organization_units'] = organization_units
        context['organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['all_organization_units_s'] = json.dumps(OrganizationUnitSerializer(
            OrganizationUnitRepo(request=request).list(), many=True).data)
        context['unit_names'] = (i[0] for i in UnitNameEnum.choices)
        context['unit_names2'] = (i[0] for i in UnitNameEnum.choices)
        materials = MaterialRepo(request=request).list()
        context['materials_s'] = json.dumps(
            MaterialSerializer(materials, many=True).data)
        services = ServiceRepo(request=request).list()
        context['services_s'] = json.dumps(
            ServiceSerializer(services, many=True).data)
        if request.user.has_perm(APP_NAME+".add_materialrequest"):
            context['materials_s'] = json.dumps(
                MaterialSerializer(materials, many=True).data)
            services = ServiceRepo(request=request).list()
            context['services_s'] = json.dumps(
                ServiceSerializer(services, many=True).data)

        context['employers']=EmployerRepo(request=request).list()
        context['project_status_enum']=(i[0] for i in ProjectStatusEnum.choices)
        context['add_project_form'] = AddProjectForm()
        context['projects'] = project.sub_projects()
        context['project_s']=json.dumps(ProjectSerializer(project).data)
        return render(request, TEMPLATE_ROOT+"project.html", context)


    def projects(self, request, *args, **kwargs):
        projects = ProjectRepo(request=request).list(*args, **kwargs)

        context = getContext(request)
        context['statuses']=(i[0] for i in ProjectStatusEnum.choices)
        employers=EmployerRepo(request=request).list()
        context['employers']=employers
        context['employers_s'] = json.dumps(EmployerSerializer(employers,many=True).data)
        context['projects'] = projects
        context['projects_s'] = json.dumps(ProjectSerializer(projects,many=True).data)
        return render(request, TEMPLATE_ROOT+"projects.html", context)


class RequestViews(View):
  
    def add_signature(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_signature_form=AddSignatureForm(request.POST)
            if add_signature_form.is_valid():
                log=3
                status=add_signature_form.cleaned_data['status']
                description=add_signature_form.cleaned_data['description']
                material_request_id=add_signature_form.cleaned_data['material_request_id']
                service_request_id=add_signature_form.cleaned_data['service_request_id']
                if material_request_id is not None:
                    log=4
                    repo=MaterialRequestRepo(request=request)
                    signature=repo.add_signature(material_request_id=material_request_id,status=status,description=description)
                    if signature is not None:
                        log=5
                        return redirect(reverse(APP_NAME+":materialrequest",kwargs={'pk':material_request_id})) 
                if service_request_id is not None:
                    log=6
                    signature=ServiceRequestRepo(request=request).add_signature(service_request_id=service_request_id,status=status,description=description)
                    if signature is not None:
                        log=7
                        return redirect(reverse(APP_NAME+":servicerequest",kwargs={'pk':service_request_id})) 

        raise Http404


class OrganizationUnitViews(View):
    def organization_units_chart(self, request, *args, **kwargs):
        context = getContext(request)
        if 'employer_id' in kwargs and kwargs['employer_id']>0:
            employer_id=kwargs['employer_id']
        else:
            employer_id=0

        employer=(EmployerRepo(request=request).employer(pk=employer_id))
        page=employer
        pages=employer.organizationunit_set.first().all_sub_pages()
        pages_s = BasicPageSerializer(pages, many=True).data
        context['pages_s'] = json.dumps(pages_s)
        return render(request, "phoenix/pages-chart.html", context)

    def getOrgUnitContext(self,request,organization_unit,*args, **kwargs):
        context={}
        context['organization_unit'] = organization_unit
        employee_repo=EmployeeRepo(request=request)
        me_employee=employee_repo.me
        can_change=False
        if me_employee in employee_repo.list(organization_unit_id=organization_unit.id):
            can_change=True
        elif request.user.has_perm(APP_NAME+".change_organizationunit"):
            can_change=True
            pass
        else:
            raise Http404

        if request.user.has_perm(APP_NAME+".add_organizationunit") or can_change:
            context['add_organization_unit_form'] = AddOrganizationUnitForm()
            all_profiles = ProfileRepo(user=request.user).objects.all()
            context['all_profiles_s'] = json.dumps(
                ProfileSerializer(all_profiles, many=True).data)
        if request.user.has_perm(APP_NAME+".add_employee") or can_change:
            context['add_employee_form'] = AddEmployeeForm()
        organization_units = organization_unit.childs()
        context['organization_units'] = organization_units 
        context['organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['all_organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        employees=EmployeeRepo(request=request).list(organization_unit_id=organization_unit.id)
        context['employees']=employees
        context['employees_s']=json.dumps(EmployeeSerializer2(employees,many=True).data)
        
        context['projects'] = organization_unit.project_set.all()
        return context

    def organization_unit(self, request, *args, **kwargs):
        organization_unit = OrganizationUnitRepo(
            request=request).organization_unit(*args, **kwargs)
        page = organization_unit
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context.update(self.getOrgUnitContext(request=request, organization_unit=organization_unit))
        return render(request, TEMPLATE_ROOT+"organization-unit.html", context)

    def employer(self, request, *args, **kwargs):
        employer = EmployerRepo(request=request).employer(*args, **kwargs)
        if employer is None:
            mv=MessageView()
            mv.message_text = "اصلاعات ناصحیح"
            mv.header_text = "خطای 452"
            return mv.response(request=request)
        context = getContext(request)
        context['employer'] = employer
        if request.user.has_perms(APP_NAME+".add_organizationunit"):
            context["add_organization_unit_form"] = AddOrganizationUnitForm()
        context['layout'] = "base-layout.html"
        context['organization_units'] = employer.organizationunit_set.all()
        return render(request, TEMPLATE_ROOT+"employer.html", context)


class EmployeeViews(View):
    def employee(self, request, *args, **kwargs):
        employee = EmployeeRepo(request=request).employee(*args, **kwargs)
        context = getContext(request)
        context.update(ProfileContext(request=request,profile=employee.profile))
        context['employee'] = employee

        context['layout'] = "base-layout.html"
        # context['selected_profile'] = employee.profile
        return render(request, TEMPLATE_ROOT+"employee.html", context)
    def dashboard(self, request, *args, **kwargs):
        employee = EmployeeRepo(request=request).employee(*args, **kwargs)
        context = getContext(request)
        context.update(ProfileContext(request=request,profile=employee.profile))
        context['employee'] = employee
        service_requests=ServiceRequestRepo(request=request).service_requests(employee_id=employee.id)
        material_requests=MaterialRequestRepo(request=request).material_requests(employee_id=employee.id)
        context['material_requests']=material_requests
        context['material_requests_s']=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        context['service_requests']=service_requests
        context['service_requests_s']=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        
        context['layout'] = "base-layout.html"
        # context['selected_profile'] = employee.profile
        return render(request, TEMPLATE_ROOT+"dashboard.html", context)

    def employees(self, request, *args, **kwargs):
        # employer_id=kwargs['employer_id'] if 'employer_id' in kwargs else 0
        # organization_unit_id=kwargs['organization_unit_id'] if 'organization_unit_id' in kwargs else 0
        employees = EmployeeRepo(request=request).list(*args, **kwargs)
        organization_unit=OrganizationUnitRepo(request=request).organization_unit(*args, **kwargs)
        employer=EmployerRepo(request=request).employer(*args, **kwargs)
        context = getContext(request)
        context['employees'] = employees
        context['employees_s']=json.dumps(EmployeeSerializer2(employees,many=True).data)
        context['organization_unit'] = organization_unit
        context['employer'] = employer
        # context['selected_profile'] = employee.profile
        return render(request, TEMPLATE_ROOT+"employees.html", context)
   

class WareHouseViews(View):
    
    def ware_house(self, request, *args, **kwargs):
        ware_house_repo=WareHouseRepo(request=request)
        ware_house = ware_house_repo.ware_house(*args, **kwargs)
        context = getContext(request)
        context.update(PageContext(request=request, page=ware_house))
        context['ware_house'] = ware_house
        context.update(OrganizationUnitViews().getOrgUnitContext(request=request, organization_unit=ware_house))
        ware_house_sheets=ware_house.sheets()
        ware_house_sheets_s=json.dumps(WareHouseSheetSerializer(ware_house_sheets,many=True).data)
        # context['materials']=ware_house_repo.materials(ware_house_id=ware_house.id)
        ware_house_materials=WareHouseMaterialRepo(request=request).list(ware_house=ware_house)
        context['ware_house_materials']=ware_house_materials
        context['ware_house_sheets_s']=ware_house_sheets_s
        context['ware_house_sheet_lines']=WareHouseSheetLineRepo(request=request).list(ware_house_id=ware_house.id).order_by('material_id')

        return render(request, TEMPLATE_ROOT+"ware-house.html", context)
 

class WareHouseSheetViews(View):
    def ware_house_import_sheet(self, request, *args, **kwargs):
        return self.ware_house_sheet(request,*args, **kwargs)
    def ware_house_export_sheet(self, request, *args, **kwargs):
        return self.ware_house_sheet(request,*args, **kwargs)
    
    def ware_house_sheet(self, request, *args, **kwargs):
        context = getContext(request)
        ware_house_sheet=WareHouseSheetRepo(request=request).ware_house_sheet(*args, **kwargs)
        context['ware_house_sheet']=ware_house_sheet
        context['page_title']="برگه انبار شماره "+str(ware_house_sheet.pk)
        context['ware_house']=ware_house_sheet.ware_house
        ware_house_sheet_lines=ware_house_sheet.sheet_lines()
        context['ware_house_sheet_lines']=ware_house_sheet_lines
        context['ware_house_sheet_lines_s']=json.dumps(WareHouseSheetLineSerializer(ware_house_sheet_lines,many=True).data)
        return render(request, TEMPLATE_ROOT+"ware-house-sheet.html", context)
    

class MaterialViews(View):
    def materials(self, request, *args, **kwargs):
        materials = MaterialRepo(request=request).list(*args, **kwargs)
        context = getContext(request)
        context['materials'] = materials
        context['materials_s'] = json.dumps(MaterialSerializer(materials,many=True).data)
        if request.user.has_perm(APP_NAME+".add_material"):
            context['add_material_form'] = AddMaterialForm()
        return render(request, TEMPLATE_ROOT+"materials.html", context)
    
    def material(self, request, *args, **kwargs):
        material = MaterialRepo(request=request).material(*args, **kwargs)
        context = getContext(request)
        context['material'] = material
        materials= material.childs()
        context['materials'] =materials 
        
        if request.user.has_perm(APP_NAME+".view_warehousesheetline"):
            ware_house_sheet_lines=WareHouseSheetLineRepo(request=request).list(material_id=material.id)
            context['ware_house_sheet_lines']=ware_house_sheet_lines

        if request.user.has_perm(APP_NAME+".view_warehousematerial"):
            ware_house_materials=WareHouseMaterialRepo(request=request).list(material_id=material.id)
            context['ware_house_materials']=ware_house_materials
        if request.user.has_perm(APP_NAME+".view_materialrequest"):
            material_requests=material.materialrequest_set.all()
            context['material_requests'] = material_requests
            context['material_requests']=MaterialRequestRepo(request=request).material_requests(material_id=material.id)
      
        context['materials_s'] = json.dumps(MaterialSerializer(materials,many=True).data)
        
        context.update(PageContext(request=request, page=material))
        if request.user.has_perm(APP_NAME+".add_material"):
            context['add_material_form'] = AddMaterialForm()
        material_requests=MaterialRequestRepo(request=request).list(material_id=material.id)
        context['material_requests']=material_requests
        context['material_requests_s']=json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        
        return render(request, TEMPLATE_ROOT+"material.html", context)


class MaterialRequestViews(View):
    def material_request(self, request, *args, **kwargs):
        me_employee=EmployeeRepo(request=request).me
        material_request = MaterialRequestRepo(request=request).material_request(*args, **kwargs)
        if material_request is None:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین درخواستی وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.response(request=request,app_name=APP_NAME,*args, **kwargs)
        if request.user.has_perm(APP_NAME+".view_materialrequest"):
            pass
        elif me_employee is not None and material_request.project in me_employee.my_projects():
            pass
        else:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین درخواستی وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.response(request=request,app_name=APP_NAME,*args, **kwargs)

        context = getContext(request)
        context['material_request'] = material_request
        context['signature_statuses']=(i[0] for i in SignatureStatusEnum.choices)
        
        context['add_signature_form']=AddSignatureForm()
        if request.user.has_perm(APP_NAME+".add_warehousesheet") and material_request.status==RequestStatusEnum.ACCEPTED:
            context['add_material_request_to_ware_house_sheet_form']=AddMaterialRequestToWareHouseSheetForm()
            context["ware_houses"]=material_request.project.contractor.ware_houses()
        return render(request, TEMPLATE_ROOT+"material-request.html", context)

    def material_requests(self, request, *args, **kwargs):
        me_employee=EmployeeRepo(request=request).me
        if request.user.has_perm(APP_NAME+".view_materialrequest"):
            material_requests = MaterialRequestRepo(request=request).material_requests(*args, **kwargs)
        
        elif me_employee is not None:
            material_requests = MaterialRequestRepo(request=request).material_requests(employee_id=me_employee.id,*args, **kwargs)
        else:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین درخواستی وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.response(request=request,app_name=APP_NAME,*args, **kwargs)

        context = getContext(request)
        context['material_requests'] = material_requests
        # context['material_requests_s'] ="[]"
        context['material_requests_s'] =json.dumps(MaterialRequestSerializer(material_requests,many=True).data)
        return render(request, TEMPLATE_ROOT+"material-requests.html", context)


class ServiceRequestViews(View):
    def service_request(self, request, *args, **kwargs):
        
        me_employee=EmployeeRepo(request=request).me
        service_request = ServiceRequestRepo(request=request).service_request(*args, **kwargs)
        if service_request is None:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین درخواستی وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.response(request=request,app_name=APP_NAME,*args, **kwargs)

        context = getContext(request)

        if request.user.has_perm(APP_NAME+".view_servicerequest"):
            pass
        elif me_employee is not None and service_request.project in me_employee.my_projects():
            pass
        else:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین درخواستی وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.show(request=request,app_name=APP_NAME)
        context['service_request'] = service_request
        context['signature_statuses']=(i[0] for i in SignatureStatusEnum.choices)
        context['add_signature_form']=AddSignatureForm()
        return render(request, TEMPLATE_ROOT+"service-request.html", context)

    def service_requests(self, request, *args, **kwargs):
        me_employee=EmployeeRepo(request=request).me
        if request.user.has_perm(APP_NAME+".view_servicerequest"):
            service_requests = ServiceRequestRepo(request=request).service_requests(*args, **kwargs)
        elif me_employee is not None:
            service_requests = ServiceRequestRepo(request=request).service_requests(employee_id=me_employee.id,*args, **kwargs)
        else:
            mv=MessageView()
            mv.header_text="خطای 404"
            mv.message_html=f"""
            <p class="text-center">
            چنین درخواستی وجود ندارد.
            </p>
            """
            mv.message_text=f"""
            """
            return mv.response(request=request,app_name=APP_NAME,*args, **kwargs)
        context = getContext(request)
        context['service_requests'] = service_requests
        context['service_requests_s'] = json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        return render(request, TEMPLATE_ROOT+"service-requests.html", context)
  

class EventViews(View):
    def eventsContext(self,request,*args, **kwargs):
        project = ProjectRepo(request=request).project(*args, **kwargs)
        context = getContext(request)
        events=project.event_set.all().order_by("event_datetime")
        context['events'] = events
        context['events_s'] = json.dumps(EventSerializerForChart(events,many=True).data)
        return context
    def event(self, request, *args, **kwargs):

        event = EventRepo(request=request).event(*args, **kwargs)
        context = getContext(request)
        context.update(PageContext(request=request, page=event))
        context['event'] = event
        context['locations']=event.locations.all()
        context['all_locations']=LocationRepo(request=request).list().order_by('title')
        if request.user.has_perm(APP_NAME+'.change_project'):
            context['add_location_form'] = AddLocationForm()
        
        if request.user.has_perm(APP_NAME+'.change_project'):
            context['add_existing_location_form'] = AddExistingLocationForm()
        return render(request, TEMPLATE_ROOT+"event.html", context)


    def project_events_chart(self, request, *args, **kwargs):
        context=self.eventsContext(request=request,*args, **kwargs)
        return render(request, TEMPLATE_ROOT+"project-events-chart.html", context)
    
    def project_events_chart2(self, request, *args, **kwargs):
        context=self.eventsContext(request=request,*args, **kwargs)
        return render(request, TEMPLATE_ROOT+"project-events-chart2.html", context)
    
    def project_events_chart3(self, request, *args, **kwargs):
        context=self.eventsContext(request=request,*args, **kwargs)
        return render(request, TEMPLATE_ROOT+"project-events-chart3.html", context)


class ServiceViews(View):
    def service(self, request, *args, **kwargs):
        service = ServiceRepo(request=request).service(*args, **kwargs)
        context = getContext(request)
        context['service'] = service
        service_requests=ServiceRequestRepo(request=request).service_requests(service_id=service.id)
        context['service_requests']=service_requests
        context['service_requests_s']=json.dumps(ServiceRequestSerializer(service_requests,many=True).data)
        context['services'] = service.childs()
        context.update(PageContext(request=request, page=service))
        context['add_service_form'] = AddServiceForm()
        return render(request, TEMPLATE_ROOT+"service.html", context)

    def services(self, request, *args, **kwargs):
        services = ServiceRepo(request=request).list(*args, **kwargs)
        context = getContext(request)
        context['services'] = services
        context['services_s'] = json.dumps(ServiceSerializer(services,many=True).data)
        return render(request, TEMPLATE_ROOT+"services.html", context)
