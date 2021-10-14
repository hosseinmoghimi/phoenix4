from django.conf.urls import url
from core.views import CoreContext
from .apps import APP_NAME
from django.shortcuts import render
from django.views import View

TEMPLATE_ROOT="help/"



def getContext(request):
    context = CoreContext(request=request, app_name=APP_NAME)    
    return context

def get_sidebar_links(app_name):
    if app_name=='projectmanager':
        from projectmanager.help import sidebar_links
    if app_name=='farm':
        from farm.help import sidebar_links
    if app_name=='mafia':
        from mafia.help import sidebar_links
    if app_name=='messenger':
        from messenger.help import sidebar_links
    return sidebar_links

class HelpView(View):

    def index(self,request,app_name,*args, **kwargs):
        context=getContext(request=request)
        context['app_name']=app_name
        context['sidebar_links']=get_sidebar_links(app_name=app_name)
        return render(request,TEMPLATE_ROOT+"index.html",context)

    def help(self,request,app_name,template,*args, **kwargs):
        context=getContext(request=request)
        context['app_name']=app_name
        context['sidebar_links']=get_sidebar_links(app_name=app_name)
        return render(request,app_name+"/help/"+template+".html",context)

        
