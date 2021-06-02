from projectmanager.serializers import MaterialSerializer
from projectmanager.models import Material, OrganizationUnit
from projectmanager.forms import AddOrganizationUnitForm, AddProjectForm
from typing import ContextManager
from django.shortcuts import render
from .forms import *
import json
from .apps import APP_NAME
from core.views import DefaultContext,PageContext
from .repo import EmployeeRepo, MaterialRepo, OrganizationUnitRepo, ProjectRepo
from django.views import View
from .utils import AdminUtility
TEMPLATE_ROOT=APP_NAME+"/"
def getContext(request):
    context=DefaultContext(request=request,app_name=APP_NAME)
    context["layout"]=TEMPLATE_ROOT+"layout.html"
    context["admin_utility"]=AdminUtility(request=request)
    context['search_action']=reverse(APP_NAME+":search")
    context['search_form']=SearchForm()
    return context


class BasicViews(View):
    def search(self,request,*args, **kwargs):
        context=getContext(request)
        log=1
        if request.method=='POST':
            log+=1
            search_form=SearchForm(request.POST)
            if search_form.is_valid():
                log+=1
                search_for=search_form.cleaned_data['search_for']
                context['search_for']=search_for
                context['materials']=MaterialRepo(request=request).list(search_for=search_for)
                context['projects']=ProjectRepo(request=request).list(search_for=search_for)
                context['organization_units']=OrganizationUnitRepo(request=request).list(search_for=search_for)
                context['log']=log
                return render(request,TEMPLATE_ROOT+"index.html",context)
        context=getContext(request)
        context['add_organization_unit_form']=AddOrganizationUnitForm()
        context['add_project_form']=AddProjectForm()
        context['projects']=ProjectRepo(request=request).list(for_home=True)
        context['materials']=MaterialRepo(request=request).list(for_home=True)
        context['organization_units']=OrganizationUnitRepo(request=request).list(for_home=True)
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['add_organization_unit_form']=AddOrganizationUnitForm()
        context['add_project_form']=AddProjectForm()
        context['projects']=ProjectRepo(request=request).list(for_home=True)
        context['materials']=MaterialRepo(request=request).list(for_home=True)
        context['organization_units']=OrganizationUnitRepo(request=request).list(for_home=True)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class ProjectViews(View):
    def project(self,request,*args, **kwargs):
        project=ProjectRepo(request).project(*args, **kwargs)   
        page=project     
        context=getContext(request)
        context.update(PageContext(request=request,page=page))
        context['project']=project
        materials=MaterialRepo(request=request).list()
        context['materials_s']=json.dumps(MaterialSerializer(materials,many=True).data)
        context['add_material_request_form']=AddMaterialRequestForm()
        context['add_project_form']=AddProjectForm()
        context['projects']=project.childs.all()
        return render(request,TEMPLATE_ROOT+"project.html",context)

class OrganizationUnitViews(View):
    def organization_unit(self,request,*args, **kwargs):
        organization_unit=OrganizationUnitRepo(request).organization_unit(*args, **kwargs)        
        page=organization_unit     
        context=getContext(request)  
        context.update(PageContext(request=request,page=page))
        context['organization_unit']=organization_unit
        context['add_organization_unit_form']=AddOrganizationUnitForm()
        context['organization_units']=organization_unit.childs.all()
        return render(request,TEMPLATE_ROOT+"organization-unit.html",context)
class EmployeeViews(View):
    def employee(self,request,*args, **kwargs):
        employee=EmployeeRepo(request).employee(*args, **kwargs)        
        context=getContext(request)  
        context['employee']=employee
        context['selected_profile']=employee.profile
        return render(request,TEMPLATE_ROOT+"employee.html",context)

class MaterialViews(View):
    def material_request(self,request,pk,*args, **kwargs):
        material_request=MaterialRepo(request).material_request(*args, **kwargs)        
        context=getContext(request)  
        context['material_request']=material_request
        return render(request,TEMPLATE_ROOT+"material-request.html",context)

    def material(self,request,pk,*args, **kwargs):
        material=MaterialRepo(request).material(*args, **kwargs)        
        context=getContext(request)  
        context['material']=material
        return render(request,TEMPLATE_ROOT+"material.html",context)
