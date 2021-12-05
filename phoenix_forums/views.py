from phoenix_forums.repo import ForumRepo
from .enums import *
from core.repo import ParameterRepo
from django.shortcuts import render
from django.shortcuts import reverse
from django.views import View
from .apps import APP_NAME
from core.views import CoreContext
TEMPLATE_ROOT=APP_NAME+'/'
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    parameter_repo=ParameterRepo(user=request.user,app_name=APP_NAME)
 
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        forums=ForumRepo(request=request).list().filter(parent=None)
        context['forums']=forums
        return render(request,TEMPLATE_ROOT+'index.html',context)
class ForumViews(View):
    def forum(self,request,*args, **kwargs):
        context=getContext(request)
        forum=ForumRepo(request=request).forum(*args, **kwargs)
        context['forum']=forum
        return render(request,TEMPLATE_ROOT+'forum.html',context)