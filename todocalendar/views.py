from django.shortcuts import render

from authentication.repo import ProfileRepo
from .repo import AppointmentRepo
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext,PageContext

from .forms import *

TEMPLATE_ROOT=APP_NAME+"/"
layout_parent='phoenix/layout.html'
def getContext(request):
    context=CoreContext(app_name='todocalendar',request=request)
    context['layout_parent']=layout_parent
    return context
# Create your views here.
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        appointments=AppointmentRepo(request=request).list()
        context['appointments']=appointments
        return render(request,TEMPLATE_ROOT+"index.html",context)
class AppointmentViews(View):
    def appointment(self,request,*args, **kwargs):
        context=getContext(request=request)
        appointment=AppointmentRepo(request=request).appointment(*args, **kwargs)
        context['appointment']=appointment
        context.update(PageContext(request=request,page=appointment))


        context['add_person_form']=AddPersonForm()
        profiles=ProfileRepo(request=request).list()
        context['profiles']=profiles
        return render(request,TEMPLATE_ROOT+"appointment.html",context)