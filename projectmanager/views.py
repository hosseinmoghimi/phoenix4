from typing import ContextManager
from django.shortcuts import render
from .apps import APP_NAME
from core.views import DefaultContext
from .repo import ProjectRepo
from django.views import View
from .utils import AdminUtility
TEMPLATE_ROOT=APP_NAME+"/"
def getContext(request):
    context=DefaultContext(request=request,app_name=APP_NAME)
    context["layout_root"]=TEMPLATE_ROOT+"/layout.html"
    context["admin_utility"]=AdminUtility(request=request)
    return context


class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['projects']=ProjectRepo(request=request).list(for_home=True)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class ProjectViews(View):
    def project(self,request,*args, **kwargs):
        if 'pk' in kwargs:
            project=ProjectRepo(request).project
        if 'project' in kwargs:
            project=kwargs['project']
        context=getContext(request)
        context['project']=project
        return render(request,TEMPLATE_ROOT+"index.html",context)