import json
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from core.serializers import DocumentSerializer
from hesabyar.enums import WareHouseSheetStatusEnum
from hesabyar.models import Transaction

from utility.persian import PersianCalendar
from .repo import ChequeRepo, CostRepo, FinancialDocumentRepo, InvoiceRepo,PaymentRepo, TransactionRepo, WageRepo, WareHouseSheetRepo
from django.http import JsonResponse
from .forms import *
from .serializers import CostSerializer, PaymentSerializer,ChequeSerializer, FinancialDocumentSerializer, InvoiceFullSerializer, InvoiceLineSerializer, WageSerializer, WareHouseSheetSerializer
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
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
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
                    pay_from_id=pay_from_id,
                    invoice_datetime=invoice_datetime,
                    pay_to_id=pay_to_id,
                    tax_percent=tax_percent,
                    ship_fee=ship_fee,
                )
                if invoice is not None:
                    context['invoice']=InvoiceFullSerializer(invoice).data
                    context['invoice_lines']=InvoiceLineSerializer(invoice.invoice_lines(),many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class TransactionApi(APIView):
    def add_transaction_document(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_document_form = AddTransactionDocumentForm(
                request.POST, request.FILES)
            if add_page_document_form.is_valid():
                log += 1
                title = add_page_document_form.cleaned_data['title']
                transaction_id = add_page_document_form.cleaned_data['transaction_id']
                file = request.FILES['file1']
                document = TransactionRepo(request=request).add_document(
                    title=title, file=file, transaction_id=transaction_id)
                if document is not None:
                    context['document'] = DocumentSerializer(
                        document, context={'request': request}).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    
class CheuqeApi(APIView):
    def add_cheque(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_cheque_form=AddChequeForm(request.POST)



            
            if add_cheque_form.is_valid():
                log=3
                fm=add_cheque_form.cleaned_data
                title=fm['title']
                cheque=ChequeRepo(request=request).add_cheque(
                    title=title,
                )
                if cheque is not None:
                    context['cheque']=ChequeSerializer(cheque).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class PaymentApi(APIView):
    def add_payment(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_payment_form=AddPaymentForm(request.POST)

            if add_payment_form.is_valid():
                log=3
                fm=add_payment_form.cleaned_data
                title=fm['title']
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
                amount=fm['amount']
                transaction_datetime=fm['transaction_datetime']
                payment_method=fm['payment_method']
                description=fm['description']
                transaction_datetime=PersianCalendar().to_gregorian(transaction_datetime+"  00:00:00")
                payment=PaymentRepo(request=request).add_payment(
                    title=title,
                    pay_to_id=pay_to_id,
                    pay_from_id=pay_from_id,
                    amount=amount,
                    transaction_datetime=transaction_datetime,
                    payment_method=payment_method,
                    description=description,
                )
                if payment is not None:
                    context['payment']=PaymentSerializer(payment).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class CostApi(APIView):
    def add_cost(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_cost_form=AddCostForm(request.POST)

            if add_cost_form.is_valid():
                log=3
                fm=add_cost_form.cleaned_data
                title=fm['title']
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
                amount=fm['amount']
                cost_type=fm['cost_type']
                transaction_datetime=fm['transaction_datetime']
                payment_method=fm['payment_method']
                description=fm['description']
                transaction_datetime=PersianCalendar().to_gregorian(transaction_datetime+"  00:00:00")
                cost=CostRepo(request=request).add_cost(
                    title=title,
                    cost_type=cost_type,
                    pay_to_id=pay_to_id,
                    pay_from_id=pay_from_id,
                    amount=amount,
                    transaction_datetime=transaction_datetime,
                    payment_method=payment_method,
                    description=description,
                )
                if cost is not None:
                    context['cost']=CostSerializer(cost).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class WageApi(APIView):
    def add_wage(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_wage_form=AddWageForm(request.POST)

            if add_wage_form.is_valid():
                log=3
                fm=add_wage_form.cleaned_data
                title=fm['title']
                pay_to_id=fm['pay_to_id']
                pay_from_id=fm['pay_from_id']
                amount=fm['amount']
                transaction_datetime=fm['transaction_datetime']
                payment_method=fm['payment_method']
                description=fm['description']
                transaction_datetime=PersianCalendar().to_gregorian(transaction_datetime+"  00:00:00")
                wage=WageRepo(request=request).add_wage(
                    title=title,
                    pay_to_id=pay_to_id,
                    pay_from_id=pay_from_id,
                    amount=amount,
                    transaction_datetime=transaction_datetime,
                    payment_method=payment_method,
                    description=description,
                )
                if wage is not None:
                    context['wage']=WageSerializer(wage).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)




class WareHouseSheetApi(APIView):
    def change_warehouse_sheet_state(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            change_warehouse_sheet_state_form=ChangeWarehouseSheetStateForm(request.POST)

            if change_warehouse_sheet_state_form.is_valid():
                log=33
                fm=change_warehouse_sheet_state_form.cleaned_data
                status=fm['status']
                if status=='DONE':
                    status=WareHouseSheetStatusEnum.DONE
                elif status=='INITIAL':
                    status=WareHouseSheetStatusEnum.INITIAL
                elif status=='IN_PROGRESS':
                    status=WareHouseSheetStatusEnum.IN_PROGRESS
                else:
                    status=WareHouseSheetStatusEnum.INITIAL

                warehouse_sheet_id=fm['warehouse_sheet_id']
                warehouse_sheet=WareHouseSheetRepo(request=request).change_state(
                    warehouse_sheet_id=warehouse_sheet_id,
                    status=status,
                )
                if warehouse_sheet is not None:
                    context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
