from django.shortcuts import render
from .apps import APP_NAME
from core.views import CoreContext
from django.views import View

# Create your views here.
LAYOUT_PARENT="phoenix/layout.html"
TEMPLATE_ROOT="hesabyar/"
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['title']="HesabYar Ver 1.0.0"
        return render(request,TEMPLATE_ROOT+"index.html",context)