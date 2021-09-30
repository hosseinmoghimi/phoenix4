from django.shortcuts import render
from core.views import CoreContext
from .apps import APP_NAME
from django.views import View

TEMPLATE_FOLDER="vehicles/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)

        return render(request,TEMPLATE_FOLDER+"index.html",context)