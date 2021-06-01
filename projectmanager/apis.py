from projectmanager.serializers import OrganizationUnitSerializer, ProjectSerializer
from core.constants import SUCCEED
from rest_framework.views import APIView
from django.http import JsonResponse
from .repo import OrganizationUnitRepo, ProjectRepo
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


class OrganizationUnitApi(APIView):
    def add_organization_unit(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_organization_unit_form=AddOrganizationUnitForm(request.POST)
            if add_organization_unit_form.is_valid():
                log+=1
                title=add_organization_unit_form.cleaned_data['title']
                parent_id=add_organization_unit_form.cleaned_data['parent_id']
                organization_unit=OrganizationUnitRepo(request=request).add_organization_unit(parent_id=parent_id,title=title)
                context['organization_unit']=OrganizationUnitSerializer(organization_unit).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
