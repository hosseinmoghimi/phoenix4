from accounting.serializers import TransactionSerializer
from accounting.repo import TransactionRepo
from accounting.forms import AddTransactionForm
from stock.models import Payment
from core.constants import FAILED,SUCCEED
from stock.serializers import DocumentSerializer,PaymentSerializer, StockSerializer
from rest_framework.views import APIView

from django.http import JsonResponse
from utility.persian import PersianCalendar



class BaseApi(APIView):
    def add_document(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log+=1
            add_transaction_form=AddTransactionForm(request.POST)
            if add_transaction_form.is_valid():
                log+=1
                title=add_transaction_form.cleaned_data['title']
                pay_to=add_transaction_form.cleaned_data['pay_to']
                pay_from=add_transaction_form.cleaned_data['pay_from']
                amount=add_transaction_form.cleaned_data['amount']
                transaction=TransactionRepo(request=request).add_transaction(title=title,pay_to=pay_to,pay_from=pay_from,amount=amount)
                context['transaction']=TransactionSerializer(transaction).data
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
                stock=StockRepo(request=request).add_stock(first_name=first_name,last_name=last_name)
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
                image=request.FILES['image']
                
                date_paid=PersianCalendar().to_gregorian(date_paid)
                payment=PaymentRepo(request=request).add_payment(title=title,value=value,date_paid=date_paid,payment_type=payment_type,stock_id=stock_id,image_origin=image)
                context['payment']=PaymentSerializer(payment).data
                context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)