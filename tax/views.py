from django.views import View
from .apps import APP_NAME
from django.shortcuts import render,reverse,redirect
from .repo import TaxRepo
from .forms import *
from core.views import CoreContext,PageContext
TEMPLATE_ROOT="tax/"
layout_parent="phoenix/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=layout_parent
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)

