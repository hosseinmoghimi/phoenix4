from django.shortcuts import render
import json
from .repo import *
from .serializers import *
from django.http import Http404
from django.views import View
from core.views import CoreContext,MessageView
from .apps import APP_NAME
TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request):
    user=request.user
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class BasicViews(View):
    def location(self,request,pk,*args, **kwargs):
        context=getContext(request)
        location=LocationRepo(request.user).location(pk)
        context['location']=location
        context['location_s']=json.dumps(LocationSerializer(location).data)

        return render(request,TEMPLATE_ROOT+"location.html",context)
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['locations']=LocationRepo(user=request.user).list()
        return render(request,TEMPLATE_ROOT+"index.html",context)
    