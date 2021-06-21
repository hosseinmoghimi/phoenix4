from django.shortcuts import render
from .apps import APP_NAME
from core.views import CoreContext, TEMPLATE_ROOT
from django.views import View
TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+'index.html',context)
# Create your views here.
