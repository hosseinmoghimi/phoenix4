from django.views import View
from core.enums import ParametersEnum

from core.repo import ParameterRepo
from .serializers import TaxSerializer
from .apps import APP_NAME
from django.shortcuts import render,reverse,redirect
from .repo import TaxRepo
from .forms import *
import json
from core.views import CoreContext,PageContext
TEMPLATE_ROOT="tax/"
layout_parent="phoenix/layout.html"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=layout_parent
    parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['app'] = {
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(ParametersEnum.TEL).value,
        'title': parameter_repo.get(ParametersEnum.TITLE).value,
    }
    return context

class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        taxes=TaxRepo(request=request).list()
        context['taxes']=taxes
        taxes_s=json.dumps(TaxSerializer(taxes,many=True).data)
        context['taxes_s']=taxes_s
        add_tax_form=AddTaxForm()
        context['add_tax_form']=add_tax_form
        return render(request,TEMPLATE_ROOT+"index.html",context)
class TaxViews(View):
    def tax(self,request,*args, **kwargs):
        context=getContext(request=request)
        tax=TaxRepo(request=request).tax(*args, **kwargs)
        context['tax']=tax
        return render(request,TEMPLATE_ROOT+"tax.html",context)

