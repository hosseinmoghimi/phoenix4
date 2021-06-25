from stock.models import Payment
from core.constants import FAILED,SUCCEED
from stock.serializers import DocumentSerializer,PaymentSerializer
from rest_framework.views import APIView
from .repo import DocumentRepo, PaymentRepo
from .forms import AddDocumentForm, AddPaymentForm
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