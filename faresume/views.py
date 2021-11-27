from django.http import request
from django.shortcuts import render,reverse

from .apps import APP_NAME
from .repo import *
from django.views import View
from core.views import CoreContext

TEMPLATE_ROOT="faresume/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request):
    context=CoreContext(app_name=APP_NAME,request=request)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    context['app']={
        'title':'resume',
        'home_url':reverse(APP_NAME+":home"),
    }
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)