import json
from urllib import request
from django.shortcuts import render,reverse
from django.utils import timezone
from authentication.repo import ProfileRepo
from core.enums import UnitNameEnum 
from .enums import CostTypeEnum, InvoicePaymentMethodEnum, PaymentMethodEnum, TransactionStatusEnum, WareHouseSheetDirectionEnum
from .forms import *

from .repo import CostRepo,GuaranteeRepo, WareHouseRepo,ChequeRepo, FinancialDocumentCategoryRepo,FinancialDocumentRepo,  InvoiceLineRepo, InvoiceRepo,  PaymentRepo, ProductRepo, FinancialAccountRepo, ServiceRepo, StoreRepo, TagRepo, WareHouseSheetRepo
from .serializers import ChequeSerializer, GuaranteeSerializer, ServiceSerializer, FinancialDocumentSerializer, InvoiceFullSerializer, InvoiceLineForProductOrServiceSerializer, InvoiceLineSerializer, ProductSerializer, WareHouseSerializer, WareHouseSheetSerializer
from .apps import APP_NAME
from core.views import CoreContext, PageContext
from django.views import View

# Create your views here.
LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "hesabyar/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class BasicViews(View):
    def search(self, request, *args, **kwargs):
        context = getContext(request)
        log = 1
        if request.method == 'POST':
            log += 1
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                log += 1
                search_for = search_form.cleaned_data['search_for']
                context['search_for'] = search_for
                financial_accounts = FinancialAccountRepo(request=request).list(search_for=search_for)
                products = ProductRepo(request=request).list(search_for=search_for)
                services = ServiceRepo(request=request).list(search_for=search_for)
                invoices = InvoiceRepo(request=request).list(search_for=search_for)
                
                
                context['financial_accounts'] = financial_accounts
                context['invoices'] = invoices
                context['products'] = products
                context['services'] = services

                if len(financial_accounts)>0  or len(products)>0  or len(services)>0  :
                    context['message']=""
                else:
                    context['message']=f"""<span class="material-icons">search_off</span> موردی پیدا نشد."""
                context['log'] = log
                return render(request, TEMPLATE_ROOT+"search.html", context)
        return BasicViews().home(request=request)
    def home(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        financial_accounts = FinancialAccountRepo(request=request).list()
        context['financial_accounts'] = financial_accounts

      
        
        return render(request, TEMPLATE_ROOT+"index.html", context)

    def tag(self, request, *args, **kwargs):
        context = getContext(request=request)
        tag = TagRepo(request=request).tag(*args, **kwargs)
        context['title'] = tag.name
        financial_accounts = FinancialAccountRepo(
            request=request).list(tag_id=tag.id)
        context['financial_accounts'] = financial_accounts
        return render(request, TEMPLATE_ROOT+"tag.html", context)

class FinancialAccountViews(View):
    def financial_account(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        financial_account = FinancialAccountRepo(
            request=request).financial_account(*args, **kwargs)
        context['financial_account'] = financial_account
        financial_documents = FinancialDocumentRepo().list(
            account_id=financial_account.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['rest']=financial_account.rest()
        if request.user.has_perm(APP_NAME+".add_financialdocumet"):
            document_categories=FinancialDocumentCategoryRepo(request=request).list()
            context['document_categories']=document_categories
            context['add_financial_document_form'] = AddFinancialDocumentForm()
        return render(request, TEMPLATE_ROOT+"financial-account.html", context)

    def financial_account_print(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        financial_account = FinancialAccountRepo(
            request=request).financial_account(*args, **kwargs)
        context['financial_account'] = financial_account
        financial_documents = FinancialDocumentRepo().list(
            account_id=financial_account.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['rest']=financial_account.rest()
        
        return render(request, TEMPLATE_ROOT+"financial-account-print.html", context)

class ProductViews(View):
    def product(self,request,*args, **kwargs):
        product=ProductRepo(request=request).product(*args, **kwargs)
        context=getContext(request=request)
        context.update(PageContext(request=request,page=product))
        
        context['product']=product
        warehouse_sheets=WareHouseSheetRepo(request=request).list(product_id=product.id).order_by('date_registered')
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context['warehouse_sheets_s']=warehouse_sheets_s


        invoice_lines=InvoiceLineRepo(request=request).list(product_id=product.id)
        invoice_lines_s=json.dumps(InvoiceLineForProductOrServiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines_s']=invoice_lines_s

        return render(request,TEMPLATE_ROOT+"product.html",context)


    def products(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"products.html",context)


class ServiceViews(View):
    def service(self,request,*args, **kwargs):
        service=ServiceRepo(request=request).service(*args, **kwargs)
        context=getContext(request=request)
        context.update(PageContext(request=request,page=service))
        
        context['service']=service


        invoice_lines=InvoiceLineRepo(request=request).list(service_id=service.id)
        invoice_lines_s=json.dumps(InvoiceLineForProductOrServiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines_s']=invoice_lines_s

        return render(request,TEMPLATE_ROOT+"service.html",context)


    def services(self,request,*args, **kwargs):
        context=getContext(request=request)
        services=ServiceRepo(request=request).list()
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        return render(request,TEMPLATE_ROOT+"services.html",context)

class ReportViews(View):
    def report(self,request,*args, **kwargs):
        context=getContext(request=request)
        end_date=timezone.now()
        from datetime import timedelta
        delta=timedelta(days=30)
        start_date=end_date-delta
        sell_benefit=12530000
        tax=1000000
        wages=5000000
        costs=1200000
        buy_service=1250000
        sell_service=3250000
        rest=0
        rest+=sell_benefit 
        rest-=wages
        rest-=buy_service
        rest+=sell_service
        rest-=tax
        rest-=costs
        context['tax']=tax
        context['wages']=wages
        context['sell_benefit']=sell_benefit
        context['start_date']=start_date
        context['end_date']=end_date
        context['buy_service']=buy_service
        context['sell_service']=sell_service
        context['costs']=costs
        context['rest']=rest

        







        buy_=25000000
        sell_=105000000
        cost_internet=250000
        cost_gas=25000
        cost_water=140000
        cost_telephone=85000
        cost_transport=132000
        cost_rent=1254000
        cost_electricity=550000
        rest_=0
        rest_+=sell_
        rest_-=cost_internet
        rest_-=cost_telephone
        rest_-=buy_
        rest_-=cost_electricity
        rest_-=cost_gas
        rest_-=cost_water
        rest_-=cost_transport
        rest_-=cost_rent

        context['buy_']=buy_
        context['sell_']=sell_
        context['cost_telephone']=cost_telephone
        context['cost_internet']=cost_internet
        context['cost_water']=cost_water
        context['cost_electricity']=cost_electricity
        context['cost_gas']=cost_gas
        context['cost_transport']=cost_transport
        context['cost_rent']=cost_rent
        context['rest_']=rest_
        return render(request,TEMPLATE_ROOT+"report.html",context)

class CostViews(View):
    def cost(self,request,*args, **kwargs):
        context=getContext(request=request)
        cost=CostRepo(request=request).cost(*args, **kwargs)
        context['cost']=cost
        context['transaction']=cost
        return render(request,TEMPLATE_ROOT+"cost.html",context)


    def new_cost(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_accounts=FinancialAccountRepo(request=request).list(*args, **kwargs)
        context['payment_methods']=(u[0] for u in PaymentMethodEnum.choices)
        context['cost_types']=(u[0] for u in CostTypeEnum.choices)
        context['financial_accounts']=financial_accounts
        
        if request.user.has_perm(APP_NAME+".add_cost"):
            context['add_cost_form']=AddCostForm()
        return render(request,TEMPLATE_ROOT+"new-cost.html",context)



class WareHouseSheetViews(View):
    def ware_house_sheet(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouse_sheet=WareHouseSheetRepo(request=request).warehouse_sheet(*args, **kwargs)
        context['warehouse_sheet']=warehouse_sheet
        return render(request,TEMPLATE_ROOT+"ware-house-sheet.html",context)

class WageViews(View):
    def wage(self,request,*args, **kwargs):
        pass
class SpendViews(View):
    def spend(self,request,*args, **kwargs):
        pass
class WareHouseViews(View):
    def ware_house(self,request,*args, **kwargs):
        print(kwargs)
        context=getContext(request=request)
        ware_house=WareHouseRepo(request=request).ware_house(*args, **kwargs)
        context['ware_house']=ware_house
        
        warehouse_sheets=WareHouseSheetRepo(request=request).list(ware_house_id=ware_house.id).order_by('date_registered')
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context['warehouse_sheets_s']=warehouse_sheets_s


        products=ProductRepo(request=request).list()
        availables_list=[]
        for product in products:    
            line=warehouse_sheets.filter(product_id=product.id).filter(ware_house=ware_house).first()
            if line is not None:
                list_item={'product':{'id':product.pk,'title':product.title,'get_absolute_url':product.get_absolute_url()}}
                list_item['available']=line.available()
                list_item['unit_name']=line.unit_name
                availables_list.append(list_item)
        context['availables_list']=json.dumps(availables_list)

        return render(request,TEMPLATE_ROOT+"ware-house.html",context)

class InvoiceViews(View):
    def buy(self,request,*args, **kwargs):
        pass
    def get_edit_invoice_context(self,request,*args, **kwargs):
        context={}
        customers=FinancialAccountRepo(request=request).list()
        context['customers']=customers

        stores=StoreRepo(request=request).list()
        context['stores']=stores
         
        
        products=ProductRepo(request=request).list()
        context['products']=products
        context['products_s']=json.dumps(ProductSerializer(products,many=True).data)


        
        services=ServiceRepo(request=request).list()
        context['services']=services
        context['services_s']=json.dumps(ServiceSerializer(services,many=True).data)

        context['unit_names']=(u[0] for u in UnitNameEnum.choices)
        context['invoice_statuses']=(u[0] for u in TransactionStatusEnum.choices)
        context['invoice_payment_methods']=(u[0] for u in InvoicePaymentMethodEnum.choices)
        
        return context
    def sell(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(self.get_edit_invoice_context(request=request))
        
        invoice=InvoiceRepo(request=request).add(*args, **kwargs)
        context['invoice']=invoice
        invoice_lines=invoice.invoice_lines()
        
        context['invoice_lines_s']=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice_s']=json.dumps(InvoiceFullSerializer(invoice).data)
        return render(request,TEMPLATE_ROOT+"edit-invoice.html",context)


        
    def edit_invoice(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(self.get_edit_invoice_context(request=request))
        
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        context['invoice']=invoice
        invoice_lines=invoice.invoice_lines()
        
        context['invoice_lines_s']=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        # customer=invoice.customer.profile
        # seller=invoice.seller.profile
        context['invoice_s']=json.dumps(InvoiceFullSerializer(invoice).data)
        return render(request,TEMPLATE_ROOT+"edit-invoice.html",context)
    def invoice_print(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        invoice_lines=invoice.invoice_lines()
        context['invoice']=invoice
        context['invoice_lines']=invoice_lines
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice_lines_s']=invoice_lines_s
        return render(request,TEMPLATE_ROOT+"invoice-print.html",context)

    def invoice_deliver(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        context['invoice']=invoice
        invoice_lines=invoice.invoice_lines()
        to_ware_house=WareHouseRepo(request=request).ware_house(owner_id=invoice.pay_to.id)
        if to_ware_house is None:
            to_ware_house=WareHouseRepo(request=request).objects.create(owner_id=invoice.pay_to.id,title="انبار "+invoice.pay_to.title)
        from_ware_house=WareHouseRepo(request=request).ware_house(owner_id=invoice.pay_from.id)
        if from_ware_house is None:
            from_ware_house=WareHouseRepo(request=request).objects.create(owner_id=invoice.pay_from.id,title="انبار "+invoice.pay_from.title)
        
        ware_house_sheet_repo=WareHouseSheetRepo(request=request)
        me=ProfileRepo(request=request).me
        for invoice_line in invoice_lines:
            warehouse_sheet=ware_house_sheet_repo.objects.filter(ware_house=to_ware_house).filter(invoice=invoice).filter(product=invoice_line.productorservice).first()
            if warehouse_sheet is None:
                warehouse_sheet=ware_house_sheet_repo.objects.create(ware_house=to_ware_house,invoice=invoice,product_id=invoice_line.productorservice.id,creator_id=me.id,direction=WareHouseSheetDirectionEnum.IMPORT,date_registered=timezone.now(),unit_name=invoice_line.unit_name,quantity=invoice_line.quantity)
            warehouse_sheet=ware_house_sheet_repo.objects.filter(ware_house=from_ware_house).filter(invoice=invoice).filter(product=invoice_line.productorservice).first()
            if warehouse_sheet is None:
                warehouse_sheet=ware_house_sheet_repo.objects.create(ware_house=from_ware_house,invoice=invoice,product_id=invoice_line.productorservice.id,creator_id=me.id,direction=WareHouseSheetDirectionEnum.EXPORT,date_registered=timezone.now(),unit_name=invoice_line.unit_name,quantity=invoice_line.quantity)
            

        
        warehouse_sheets=WareHouseSheetRepo(request=request).list(invoice_id=invoice.id).order_by('date_registered')
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context['warehouse_sheets_s']=warehouse_sheets_s


        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        
        return render(request,TEMPLATE_ROOT+"invoice-deliver.html",context)
    
    def invoice_guarantees(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        context['invoice']=invoice
        invoice_lines=invoice.invoice_lines()
        
        guarantee_repo=GuaranteeRepo(request=request)
        me=ProfileRepo(request=request).me
         
        for invoice_line in invoice_lines:
            for i in range(int(invoice_line.quantity)):
                guarantee=guarantee_repo.objects.filter(invoice=invoice).filter(serial_no=str(i+1)).filter(product=invoice_line.productorservice).first()
                if guarantee is None:
                    guarantee=guarantee_repo.objects.create(invoice=invoice,serial_no=str(i+1),product_id=invoice_line.productorservice.id,start_date=timezone.now(),end_date=timezone.now())
            
        
        guarantees=guarantee_repo.list(invoice_id=invoice.id)
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s


        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        
        return render(request,TEMPLATE_ROOT+"invoice-guarantees.html",context)

    def invoice(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=InvoiceRepo(request=request).invoice(*args, **kwargs)
        invoice_lines=invoice.invoice_lines()
        context['invoice']=invoice
        context['invoice_lines']=invoice_lines
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice_lines_s']=invoice_lines_s
        return render(request,TEMPLATE_ROOT+"invoice.html",context)
    def invoices(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoices=InvoiceRepo(request=request).list(*args, **kwargs)
        context['invoices']=invoices
        return render(request,TEMPLATE_ROOT+"invoices.html",context)
class FinancialDocumentViews(View):
    
    def financial_document(self, request, *args, **kwargs):
        context = getContext(request=request)
        financial_document = FinancialDocumentRepo().financial_document(*args, **kwargs)
        context['financial_document'] = financial_document
        return render(request, TEMPLATE_ROOT+"financial-document.html", context)

    def financial_document_category(self, request, *args, **kwargs):
        context = getContext(request=request)
        financial_document_category=FinancialDocumentCategoryRepo(request=request).financial_document_category(*args, **kwargs)
        financial_documents = FinancialDocumentRepo().list(
            category_id=financial_document_category.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['financial_document_category'] = financial_document_category
        context['rest']=0
        return render(request, TEMPLATE_ROOT+"financial-document-category.html", context)

    def getFinancialDocumentContext(self,request,financial_document):
        context=PageContext(request=request,page=financial_document)
        context['financial_document']=financial_document
        return context
    def financial_documents(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_documents=FinancialDocumentRepo(request=request).list()
        context['financial_documents']=financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        rest=0
        for doc in financial_documents:
            rest=rest+doc.bedehkar-doc.bestankar
        context['rest']=rest
        return render(request,TEMPLATE_ROOT+"financial-documents.html",context)
    def invoice_financial_document(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice_financial_document=FinancialDocumentRepo(request=request).invoice_financial_document(*args, **kwargs)
        invoice=invoice_financial_document.invoice
        context.update(self.getFinancialDocumentContext(request=request,financial_document=invoice_financial_document))
        invoice_lines=invoice.invoice_lines()
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice']=invoice
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s
        return render(request,TEMPLATE_ROOT+"invoice-financial-document.html",context)
     
class BankAccountViews(View):
    def bank_account(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice_financial_document=FinancialDocumentRepo(request=request).financial_document(*args, **kwargs)
        invoice=invoice_financial_document.invoice
        invoice_lines=invoice.invoice_lines()
        invoice_lines_s=json.dumps(InvoiceLineSerializer(invoice_lines,many=True).data)
        context['invoice']=invoice
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s
        return render(request,TEMPLATE_ROOT+"invoice.html",context)
class StoreViews(View):
    def store(self,request,*args, **kwargs):
        context=getContext(request=request)
        store=StoreRepo(request=request).store(*args, **kwargs)
        context['store']=store
        return render(request,TEMPLATE_ROOT+"store.html",context)
class ChequeViews(View):
    def cheque(self,request,*args, **kwargs):
        context=getContext(request=request)
        cheque=ChequeRepo(request=request).cheque(*args, **kwargs)
        context['cheque']=cheque
        return render(request,TEMPLATE_ROOT+"cheque.html",context)
    def cheques(self,request,*args, **kwargs):
        context=getContext(request=request)
        cheques=ChequeRepo(request=request).list()
        cheques_s=json.dumps(ChequeSerializer(cheques,many=True).data)
        context['cheques_s']=cheques_s
        if request.user.has_perm(APP_NAME+".add_cheque"):
            context['add_cheque_form']=AddChequeForm()
        return render(request,TEMPLATE_ROOT+"cheques.html",context)

class PaymentViews(View):
    def new_payment(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_accounts=FinancialAccountRepo(request=request).list(*args, **kwargs)
        context['payment_methods']=(u[0] for u in PaymentMethodEnum.choices)
        context['financial_accounts']=financial_accounts
        if request.user.has_perm(APP_NAME+".add_payment"):
            context['add_payment_form']=AddPaymentForm()
        return render(request,TEMPLATE_ROOT+"new-payment.html",context)
    def payments(self,request,*args, **kwargs):
        context=getContext(request=request)
        payments=PaymentRepo(request=request).list()
        context['payments']=payments
        return render(request,TEMPLATE_ROOT+"payments.html",context)
    def payment(self,request,*args, **kwargs):
        context=getContext(request=request)
        payment=PaymentRepo(request=request).payment(*args, **kwargs)
        context['payment']=payment
        context['transaction']=payment
        return render(request,TEMPLATE_ROOT+"payment.html",context)
    


class GuaranteeViews(View):
    def guarantee(self,request,*args, **kwargs):
        context=getContext(request=request)
        guarantee=GuaranteeRepo(request=request).guarantee(*args, **kwargs)
        context['guarantee']=guarantee
        return render(request,TEMPLATE_ROOT+"guarantee.html",context)
    
    
    def guarantees(self,request,*args, **kwargs):
        context=getContext(request=request)
        guarantees=GuaranteeRepo(request=request).list(*args, **kwargs)
        context['guarantees']=guarantees
        guarantees_s=json.dumps(GuaranteeSerializer(guarantees,many=True).data)
        context['guarantees_s']=guarantees_s
        return render(request,TEMPLATE_ROOT+"guarantees.html",context)
    
    