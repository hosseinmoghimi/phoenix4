from stock.serializers import AgentSerializer, StockSerializer
from .utils import AdminUtility
from core.settings import SITE_URL
from .forms import *
from .enums import *
from core.repo import ParameterRepo
from django.shortcuts import render
from django.shortcuts import reverse
from django.views import View
from .apps import APP_NAME
from .repo import AgentRepo, DocumentRepo, StockRepo
from core.views import CoreContext
import json
import os
from django.http import HttpResponse,Http404
TEMPLATE_ROOT=APP_NAME+'/'
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    parameter_repo=ParameterRepo(user=request.user,app_name=APP_NAME)
    context['search_form']=SearchForm()
    context['search_action']=reverse(APP_NAME+":search")
    context['admin_utility']=AdminUtility()
 
    parameter_repo=ParameterRepo(app_name=APP_NAME,request=request)
    context['stock1']=parameter_repo.parameter(name=ParametersEnum.STOCK1)
    context['stock2']=parameter_repo.parameter(name=ParametersEnum.STOCK2)
    return context
class BasicViews(View):
    def search(self,request,*args, **kwargs):
        if request.method=='POST':
            search_form=SearchForm(request.POST,request.FILES)
            if search_form.is_valid():
                search_for=search_form.cleaned_data['search_for']
                context=getContext(request)
                stocks=StockRepo(request=request).list(search_for=search_for)
                context['stocks']=stocks
                context['stocks_s']=json.dumps(StockSerializer(stocks,many=True).data)
                agents=AgentRepo(request=request).list(search_for=search_for)
                context['agents']=agents
                context['agents_s']=json.dumps(AgentSerializer(agents,many=True).data)
                return render(request,TEMPLATE_ROOT+'index.html',context)
        return self.home(request=request,*args, **kwargs)
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        stocks=StockRepo(request=request).list()
        agents=AgentRepo(request=request).list()
        context['stocks']=stocks
        context['stocks_s']=json.dumps(StockSerializer(stocks,many=True).data)
        context['agents']=agents
        context['agents_s']=json.dumps(AgentSerializer(agents,many=True).data)
        context['add_stock_form']=AddStockForm()
        return render(request,TEMPLATE_ROOT+'index.html',context)
class StockViews(View):
    def stock(self,request,*args, **kwargs):
        context=getContext(request)
        stock=StockRepo(request=request).stock(*args, **kwargs)
        context['stock']=stock
        if request.user.has_perm(APP_NAME+".stock.add_document"):
            context['add_document_form']=AddDocumentForm()
        if request.user.has_perm(APP_NAME+".stock.add_payment"):
            context['add_payment_form']=AddPaymentForm()
            context['payment_types']=(ii[0] for ii in PaymentTypeEnum.choices)
        context['documents']=stock.document_set.all()
        context['payments']=stock.payment_set.order_by('date_paid')
        return render(request,TEMPLATE_ROOT+'stock.html',context)
    def agent(self,request,*args, **kwargs):
        context=getContext(request)
        stocks=StockRepo(request=request).list(*args, **kwargs)
        context['stocks']=stocks
        context['stocks_s']=json.dumps(StockSerializer(stocks,many=True).data)
        return render(request,TEMPLATE_ROOT+'agent.html',context)
class DocumentViews(View):
    def get_download_response(self,request,*args, **kwargs):
        document=DocumentRepo(request=request).document(*args, **kwargs)
        file_path = str(document.file.path)
        # return JsonResponse({'download:':str(file_path)})
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
        from log.repo import LogRepo
        LogRepo(request=request).add_log(title="Http404 stock views 1",app_name=APP_NAME) 
        raise Http404
