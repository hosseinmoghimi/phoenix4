from django.shortcuts import render
from .repo import *
from django.views import View
from core.views import CoreContext

TEMPLATE_ROOT="authentication/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class ProfileViews(View):
    def profile(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+"profile.html",context)