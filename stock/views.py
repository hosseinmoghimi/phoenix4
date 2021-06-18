from .enums import ParametersEnum
from core.repo import ParameterRepo
from django.shortcuts import render
from django.views import View
from .apps import APP_NAME
from .repo import StockRepo
from core.views import CoreContext
TEMPLATE_ROOT=APP_NAME+'/'
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['stock1']=ParameterRepo(app_name=APP_NAME,user=request.user).get(name=ParametersEnum.STOCK1)
    context['stock2']=ParameterRepo(app_name=APP_NAME,user=request.user).get(name=ParametersEnum.STOCK2)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        stocks=StockRepo(request=request).list()
        context['stocks']=stocks
        return render(request,TEMPLATE_ROOT+'index.html',context)