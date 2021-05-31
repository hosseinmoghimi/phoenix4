from django.shortcuts import render
from .apps import APP_NAME
from .settings import *
from .enums import *
from .constants import *
# Create your views here.
def CoreContext(request,app_name,*args, **kwargs):
    context={}
    context['user']=request.user
    context['APP_NAME']=app_name
    
    context[app_name+'_sidebar']=True
    context['DEBUG']=DEBUG
    context['ADMIN_URL']=ADMIN_URL
    context['MEDIA_URL']=MEDIA_URL
    context['SITE_URL']=SITE_URL
    context['CURRENCY']=CURRENCY
    context['PUSHER_IS_ENABLE']=PUSHER_IS_ENABLE

    return context
def DefaultContext(request,app_name='core'):
    context=CoreContext(request=request,app_name=app_name)
    return context