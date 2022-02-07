import json
from pydoc import doc
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView

from utility.persian import PersianCalendar
from .repo import FinancialDocumentRepo, InvoiceRepo
from django.http import JsonResponse
from .forms import *
from .serializers import FinancialDocumentSerializer, InvoiceFullSerializer, InvoiceLineSerializer
class BasicApi(APIView):
    def add_financial_document(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_financial_document_form=AddFinancialDocumentForm(request.POST)



            
            if add_financial_document_form.is_valid():
                log=3
                fm=add_financial_document_form.cleaned_data
                title=fm['title']
                bestankar=fm['bestankar']
                bedehkar=fm['bedehkar']
                document_datetime=fm['document_datetime']
                account_id=fm['account_id']
                category_id=fm['category_id']
                document_datetime=PersianCalendar().to_gregorian(document_datetime)
                financial_document=FinancialDocumentRepo(request=request).add_financial_document(
                    title=title,
                    bestankar=bestankar,
                    account_id=account_id,
                    bedehkar=bedehkar,
                    document_datetime=document_datetime,
                    category_id=category_id,
                )
                if financial_document is not None:
                    context['rest']=financial_document.account.rest()
                    context['financial_document']=FinancialDocumentSerializer(financial_document).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

    def edit_invoice(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            edit_invoice_form=EditInvoiceForm(request.POST)



            
            if edit_invoice_form.is_valid():
                log=3
                fm=edit_invoice_form.cleaned_data
                lines=fm['lines']
                lines=json.loads(lines)
                seller_id=fm['seller_id']
                customer_id=fm['customer_id']
                invoice_datetime=fm['invoice_datetime']
                ship_fee=fm['ship_fee']
                tax_percent=fm['tax_percent']
                description=fm['description']
                discount=fm['discount']
                invoice_id=fm['invoice_id']
                payment_method=fm['payment_method']
                status=fm['status']
                invoice_datetime=PersianCalendar().to_gregorian(invoice_datetime)
                invoice=InvoiceRepo(request=request).edit_invoice(
                    invoice_id=invoice_id,
                    lines=lines,
                    status=status,
                    payment_method=payment_method,
                    description=description,
                    discount=discount,
                    customer_id=customer_id,
                    invoice_datetime=invoice_datetime,
                    seller_id=seller_id,
                    tax_percent=tax_percent,
                    ship_fee=ship_fee,
                )
                if invoice is not None:
                    context['invoice']=InvoiceFullSerializer(invoice).data
                    context['invoice_lines']=InvoiceLineSerializer(invoice.invoice_lines(),many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
