from messenger.repo import MessageRepo
from messenger.models import Message
from django.core.checks import messages
from django.shortcuts import render
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext

from messenger import apps
TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context



class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        messages=MessageRepo(request=request).list(for_home=True,*args, **kwargs)
        context['messages']=MessageRepo(request=request).objects.all()
        context['messages']=messages
        return render(request,TEMPLATE_ROOT+"index.html",context)
class MessageViews(View):
    def message(self,request,*args, **kwargs):
        context=getContext(request=request)
        message=MessageRepo(request=request).message(*args, **kwargs)
        context['message']=message
        return render(request,TEMPLATE_ROOT+"message.html",context)

  