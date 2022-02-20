from django.shortcuts import render
from core.views import CoreContext
from django.views import View
from .repo import LogRepo
from log.apps import APP_NAME
TEMPLATE_ROOT="log/"
LAYOUT_PARENT="phoenix/layout.html"
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context



class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class LogViews(View):
    def log(self,request,*args, **kwargs):
        context=getContext(request=request)
        log=LogRepo(request=request).log(*args, **kwargs)
        context['log']=log
        return render(request,TEMPLATE_ROOT+"log.html",context)