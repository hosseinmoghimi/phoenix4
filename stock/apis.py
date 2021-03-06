from stock.models import Payment
from core.constants import FAILED,SUCCEED
from stock.serializers import DocumentSerializer,PaymentSerializer, StockSerializer
from rest_framework.views import APIView
from .repo import DocumentRepo, PaymentRepo, StockRepo
from .forms import AddDocumentForm, AddPaymentForm, AddStockForm
from django.http import JsonResponse
from utility.persian import PersianCalendar



class DocumentApi(APIView):
    def add_document(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_document_form=AddDocumentForm(request.POST,request.FILES)
            if add_document_form.is_valid():
                log+=1
                title=add_document_form.cleaned_data['title']
                stock_id=add_document_form.cleaned_data['stock_id']
                file=request.FILES['file']      
                document=DocumentRepo(request=request).add_document(title=title,stock_id=stock_id,file=file)
                context['document']=DocumentSerializer(document).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


        
class StockApi(APIView):
    def add_stock(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_stock_form=AddStockForm(request.POST)
            if add_stock_form.is_valid():
                log+=1
                first_name=add_stock_form.cleaned_data['first_name']
                last_name=add_stock_form.cleaned_data['last_name']
                stock1=add_stock_form.cleaned_data['stock1']
                stock2=add_stock_form.cleaned_data['stock2']
                agent_id=add_stock_form.cleaned_data['agent_id']
                stock=StockRepo(request=request).add_stock(agent_id=agent_id,first_name=first_name,last_name=last_name,stock1=stock1,stock2=stock2)
                context['stock']=StockSerializer(stock).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


        
class PaymentApi(APIView):
    def add_payment(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_payment_form=AddPaymentForm(request.POST,request.FILES)
            if add_payment_form.is_valid():
                log+=1
                title=add_payment_form.cleaned_data['title']
                value=add_payment_form.cleaned_data['value']
                date_paid=add_payment_form.cleaned_data['date_paid']
                payment_type=add_payment_form.cleaned_data['payment_type']
                stock_id=add_payment_form.cleaned_data['stock_id']
                try:
                    image=request.FILES['image']    
                except:
                    image=None
                date_paid=PersianCalendar().to_gregorian(date_paid)
                payment=PaymentRepo(request=request).add_payment(title=title,value=value,date_paid=date_paid,payment_type=payment_type,stock_id=stock_id,image_origin=image)
                context['payment']=PaymentSerializer(payment).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)