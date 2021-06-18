from django.shortcuts import render
from django.views import View
from .apps import APP_NAME
from .repo import StockRepo
from core.views import CoreContext
TEMPLATE_ROOT=APP_NAME+'/'
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+'index.html',context)