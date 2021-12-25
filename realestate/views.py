from authentication.views import ProfileContext
from realestate.utils import AdminUtility
from core.enums import ParametersEnum
from core.repo import ParameterRepo
from realestate.models import Property
from django.shortcuts import render,reverse
from .apps import APP_NAME
from core.views import CoreContext, TEMPLATE_ROOT
from django.views import View
from .repo import CarRepo, PropertyRepo
TEMPLATE_ROOT="realestate_new/"
TEMPLATE_ROOT=APP_NAME+"/"
layout_parent="phoenix/layout.html"
layout_parent="realestate/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=layout_parent
    context['SITE_TITLE']=ParameterRepo(app_name=APP_NAME,request=request).parameter(name="عنوان بنگاه").value
    parameter_repo = ParameterRepo(app_name=APP_NAME)
    context['admin_utility']=AdminUtility()
  
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        properties=PropertyRepo(request=request).list()
        context['properties']=properties
        return render(request,TEMPLATE_ROOT+'index.html',context)
    def agent(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(ProfileContext(request=request,profile_id=kwargs['pk']))
        context['agent']=context['selected_profile']
        return render(request,TEMPLATE_ROOT+'agent.html',context)
class PropertyViews(View):
    def property_media(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+'property-media.html',context)
    def property(self,request,*args, **kwargs):
        context=getContext(request=request)
        property=PropertyRepo(request=request).property(*args, **kwargs)
        context['property']=property
        return render(request,TEMPLATE_ROOT+'property.html',context)
class CarViews(View):
    def car(self,request,*args, **kwargs):
        context=getContext(request=request)
        car=CarRepo(request=request).car(*args, **kwargs)
        context['car']=car
        return render(request,TEMPLATE_ROOT+'car.html',context)
# Create your views here.
