from django.shortcuts import render
from .apps import APP_NAME
from core.views import CoreContext

from django.views import View
from .repo import RelayRepo
TEMPLATE_ROOT="bms/"
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)

    


