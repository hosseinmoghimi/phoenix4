from django.shortcuts import render
from core.views import CoreContext
from .apps import APP_NAME

TEMPLATE_ROOT="dashboard/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
# Create your views here.
class BasicViews():
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)