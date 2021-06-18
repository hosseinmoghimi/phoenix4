from core.settings import SITE_URL
from .enums import *
from core.repo import ParameterRepo
from django.shortcuts import render
from django.shortcuts import reverse
from django.views import View
from .apps import APP_NAME
from .repo import StockRepo
from core.views import CoreContext
TEMPLATE_ROOT=APP_NAME+'/'
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    parameter_repo=ParameterRepo(user=request.user,app_name=APP_NAME)
    context['app'] = {
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(CoreEnums.ParametersEnum.TEL).value,
        'title': parameter_repo.get(CoreEnums.ParametersEnum.TITLE).value,
    }
    context['stock1']=ParameterRepo(app_name=APP_NAME,user=request.user).get(name=ParametersEnum.STOCK1)
    context['stock2']=ParameterRepo(app_name=APP_NAME,user=request.user).get(name=ParametersEnum.STOCK2)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        stocks=StockRepo(request=request).list()
        context['stocks']=stocks
        return render(request,TEMPLATE_ROOT+'index.html',context)
class StockViews(View):
    def stock(self,request,*args, **kwargs):
        context=getContext(request)
        stock=StockRepo(request=request).stock(*args, **kwargs)
        context['stock']=stock
        return render(request,TEMPLATE_ROOT+'stock.html',context)
    def agent(self,request,*args, **kwargs):
        context=getContext(request)
        stocks=StockRepo(request=request).list(*args, **kwargs)
        context['stocks']=stocks
        return render(request,TEMPLATE_ROOT+'index.html',context)