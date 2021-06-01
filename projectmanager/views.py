from projectmanager.forms import AddOrganizationUnitForm, AddProjectForm
from typing import ContextManager
from django.shortcuts import render
from .apps import APP_NAME
from core.views import DefaultContext,PageContext
from .repo import EmployeeRepo, MaterialRepo, OrganizationUnitRepo, ProjectRepo
from django.views import View
from .utils import AdminUtility
TEMPLATE_ROOT=APP_NAME+"/"
def getContext(request):
    context=DefaultContext(request=request,app_name=APP_NAME)
    context["layout_root"]=TEMPLATE_ROOT+"layout.html"
    context["admin_utility"]=AdminUtility(request=request)
    return context


class BasicViews(View):
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
    def employee(self,request,pk,*args, **kwargs):
        employee=EmployeeRepo(request).employee(*args, **kwargs)        
        context=getContext(request)  
        context['employee']=employee
        return render(request,TEMPLATE_ROOT+"employee.html",context)

class MaterialViews(View):
    def material(self,request,pk,*args, **kwargs):
        material=MaterialRepo(request).material(*args, **kwargs)        
        context=getContext(request)  
        context['material']=material
        return render(request,TEMPLATE_ROOT+"material.html",context)
