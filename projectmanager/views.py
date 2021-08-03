from web.repo import CarouselRepo
from utility.persian import PersianCalendar
from authentication.repo import ProfileRepo
from authentication.serilizers import ProfileSerializer
from core.serializers import BasicPageSerializer
from projectmanager.enums import ProjectStatusEnum, SignatureStatusEnum, UnitNameEnum
from core.enums import AppNameEnum, ParametersEnum
from core.repo import ParameterRepo, PictureRepo
from projectmanager.serializers import MaterialSerializer, OrganizationUnitSerializer, ProjectSerializer, ServiceSerializer
from projectmanager.models import Material, OrganizationUnit
from projectmanager.forms import AddOrganizationUnitForm, AddProjectForm
from typing import ContextManager
from django.shortcuts import render
from .forms import *
import json
from .apps import APP_NAME
from core.views import DefaultContext, PageContext
from .repo import EmployeeRepo, EmployerRepo, EventRepo, MaterialRepo, OrganizationUnitRepo, ProjectRepo, ServiceRepo
from django.views import View
from .utils import AdminUtility
TEMPLATE_ROOT = APP_NAME+"/"


def getContext(request):
    context = DefaultContext(request=request, app_name=APP_NAME)
    context["layout"] = TEMPLATE_ROOT+"layout.html"
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
                context['events'] = EventRepo(
                    request=request).search(search_for=search_for)
                context['organization_units'] = OrganizationUnitRepo(
                    request=request).list(search_for=search_for)
                context['log'] = log
                return render(request, TEMPLATE_ROOT+"search.html", context)

    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['parent_id'] = 0
        picture_repo=PictureRepo(request=request,app_name=APP_NAME)
        carousel_repo=CarouselRepo(request=request,app_name=APP_NAME)
        splash=picture_repo.get(name="index.splash")
        context['splash']=splash
        carousels=carousel_repo.list()
        if len(carousels)>0:
            context['carousels']=carousels
        context['add_service_form'] = AddServiceForm()
        context['add_organization_unit_form'] = AddOrganizationUnitForm()
        context['add_employer_form'] = AddEmployerForm()
        context['add_material_form'] = AddMaterialForm()
        context['add_project_form'] = AddProjectForm()
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
    def projects_chart(self, request, *args, **kwargs):
        context = getContext(request)
        if 'pk' in kwargs and kwargs['pk']>0:
            pk=kwargs['pk']
        else:
            pk=0

        page=(ProjectRepo(request=request).project(pk=pk))
        pages=page.all_sub_pages()
        pages_s = BasicPageSerializer(pages, many=True).data
        context['pages_s'] = json.dumps(pages_s)
        return render(request, "dashboard/pages-chart.html", context)

    

    def project_materials_order(self, request, *args, **kwargs):
        context = getContext(request)
        TAX_PERCENT = 0
        project = ProjectRepo(request).project(*args, **kwargs)
        lines = []
        lines_total = 0
        for material_request in project.materialrequest_set.all():
            quantity = material_request.quantity
            unit_name = material_request.unit_name
            unit_price = material_request.unit_price
            lines_total += (quantity*unit_price)
            lines.append({
                'quantity': quantity,
                'unit_name': unit_name,
                'unit_price': unit_price,
                'line_total': quantity*unit_price,
                'product': material_request.material,
            })

        tax = int(TAX_PERCENT*(lines_total)/100)
        ship_fee = 0
        description = f"""مربوط به {project.full_title}"""
        total_for_pay = tax+lines_total
        print_date = PersianCalendar().date
        order = {
            'customer': project.employer,
            'supplier': project.contractor,
            'orderline_set': {
                'all': lines,
            },
            'tax': tax,
            'lines_total': lines_total,
            'ship_fee': ship_fee,
            'total_for_pay': total_for_pay,
            'print_date': print_date,
            'description': description,
        }
        context['order'] = order
        context['project'] = project
        return render(request, TEMPLATE_ROOT+"order.html", context)

    def project_services_order(self, request, *args, **kwargs):
        context = getContext(request)
        TAX_PERCENT = 0
        project = ProjectRepo(request).project(*args, **kwargs)
        lines = []
        lines_total = 0
        for service_request in project.servicerequest_set.all():
            quantity = service_request.quantity
            unit_name = service_request.unit_name
            unit_price = service_request.unit_price
            lines_total += (quantity*unit_price)
            lines.append({
                'quantity': quantity,
                'unit_name': unit_name,
                'unit_price': unit_price,
                'line_total': quantity*unit_price,
                'product': service_request.service,
            })

        tax = int(TAX_PERCENT*(lines_total)/100)
        ship_fee = 0
        description = f"""مربوط به {project.full_title}"""
        print(description)
        print(10*"#1045374346#")
        total_for_pay = tax+lines_total
        print_date = PersianCalendar().date
        order = {
            'customer': project.employer,
            'supplier': project.contractor,
            'orderline_set': {
                'all': lines,
            },
            'tax': tax,
            'lines_total': lines_total,
            'ship_fee': ship_fee,
            'total_for_pay': total_for_pay,
            'print_date': print_date,
            'description': description,
        }
        context['order'] = order
        context['project'] = project
        return render(request, TEMPLATE_ROOT+"order.html", context)

    def project(self, request, *args, **kwargs):
        project = ProjectRepo(request).project(*args, **kwargs)
        page = project
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['project'] = project
        
        if request.user.has_perm(APP_NAME+'.change_project'):
            context['add_location_form'] = AddLocationForm()
        
        if request.user.has_perm(APP_NAME+'.add_event'):
            context['add_event_form'] = AddEventForm()
        context['edit_project_form']=EditProjectForm()
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
        context['add_material_request_form'] = AddMaterialRequestForm()
        context['add_service_request_form'] = AddServiceRequestForm()
        context['employers']=EmployerRepo(request=request).list()
        context['project_status_enum']=(i[0] for i in ProjectStatusEnum.choices)
        context['add_project_form'] = AddProjectForm()
        context['projects'] = project.sub_projects()
        context['project_s']=json.dumps(ProjectSerializer(project).data)
        return render(request, TEMPLATE_ROOT+"project.html", context)


class OrganizationUnitViews(View):
    def organization_unit(self, request, *args, **kwargs):
        organization_unit = OrganizationUnitRepo(
            request).organization_unit(*args, **kwargs)
        page = organization_unit
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['organization_unit'] = organization_unit
        context['add_organization_unit_form'] = AddOrganizationUnitForm()
        context['organization_units'] = organization_unit.childs()
        organization_units = organization_unit.childs()
        context['organization_units'] = organization_units
        context['add_employee_form'] = AddEmployerForm()
        all_profiles = ProfileRepo(user=request.user).objects.all()
        context['all_profiles_s'] = json.dumps(
            ProfileSerializer(all_profiles, many=True).data)
        context['organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)
        context['all_organization_units_s'] = json.dumps(
            OrganizationUnitSerializer(organization_units, many=True).data)

        context['projects'] = organization_unit.project_set.all()
        return render(request, TEMPLATE_ROOT+"organization-unit.html", context)

    def employer(self, request, *args, **kwargs):
        employer = EmployerRepo(request).employer(*args, **kwargs)
        context = getContext(request)
        context['employer'] = employer
        if request.user.has_perms(APP_NAME+".add_organizationunit"):
            context["add_organization_unit_form"] = AddOrganizationUnitForm()
        context['layout'] = "base-layout.html"
        context['organization_units'] = employer.organizationunit_set.all()
        return render(request, TEMPLATE_ROOT+"employer.html", context)


class EmployeeViews(View):
    def employee(self, request, *args, **kwargs):
        employee = EmployeeRepo(request).employee(*args, **kwargs)
        context = getContext(request)
        context['employee'] = employee

        context['layout'] = "base-layout.html"
        context['selected_profile'] = employee.profile
        return render(request, TEMPLATE_ROOT+"employee.html", context)


class MaterialViews(View):
    def material_request(self, request, *args, **kwargs):
        material_request = MaterialRepo(request).material_request(*args, **kwargs)
        context = getContext(request)
        context['material_request'] = material_request
        context['signature_statuses']=(i[0] for i in SignatureStatusEnum.choices)
        return render(request, TEMPLATE_ROOT+"material-request.html", context)

    def material(self, request, *args, **kwargs):
        material = MaterialRepo(request).material(*args, **kwargs)
        context = getContext(request)
        context['material'] = material
        context['materials'] = material.childs()
        context.update(PageContext(request=request, page=material))
        context['add_material_form'] = AddMaterialForm()
        return render(request, TEMPLATE_ROOT+"material.html", context)


class EventViews(View):
    def event(self, request, *args, **kwargs):
        event = EventRepo(request).event(*args, **kwargs)
        context = getContext(request)
        context.update(PageContext(request=request, page=event))
        context['event'] = event
        return render(request, TEMPLATE_ROOT+"event.html", context)


class ServiceViews(View):
    def service_request(self, request, *args, **kwargs):
        service_request = ServiceRepo(request).service_request(*args, **kwargs)
        context = getContext(request)
        context['service_request'] = service_request
        context['signature_statuses']=(i[0] for i in SignatureStatusEnum.choices)
        return render(request, TEMPLATE_ROOT+"service-request.html", context)

    def service(self, request, *args, **kwargs):
        service = ServiceRepo(request).service(*args, **kwargs)
        context = getContext(request)
        context['service'] = service
        context['services'] = service.childs()
        context.update(PageContext(request=request, page=service))
        context['add_service_form'] = AddServiceForm()
        return render(request, TEMPLATE_ROOT+"service.html", context)
