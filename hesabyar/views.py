import json
from django.shortcuts import redirect, render,reverse
from django.utils import timezone
from authentication.repo import ProfileRepo
from core.enums import UnitNameEnum
from .repo import TagRepo
from core.serializers import DocumentSerializer
from hesabyar.models import TransactionCategory 
from .enums import CostTypeEnum, InvoicePaymentMethodEnum, PaymentMethodEnum, TransactionStatusEnum, WareHouseSheetDirectionEnum
from .forms import *

from .repo import CostRepo,GuaranteeRepo, SpendRepo, TransactionCategoryRepo, TransactionRepo, WageRepo, WareHouseRepo,ChequeRepo, FinancialDocumentCategoryRepo,FinancialDocumentRepo,  InvoiceLineRepo, InvoiceRepo,  PaymentRepo, ProductRepo, FinancialAccountRepo, ServiceRepo, StoreRepo, WareHouseSheetRepo
from .serializers import ChequeSerializer, FinancialDocumentForAccountSerializer, GuaranteeSerializer, ServiceSerializer, FinancialDocumentSerializer, InvoiceFullSerializer, InvoiceLineForProductOrServiceSerializer, InvoiceLineSerializer, ProductSerializer, SpendSerializer, TransactionSerializer, WareHouseSerializer, WareHouseSheetSerializer
from .apps import APP_NAME
from core.views import CoreContext, MessageView, PageContext
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
        context['tag'] = tag
        financial_accounts = FinancialAccountRepo(request=request).list(tag_id=tag.id)
        context['financial_accounts'] = financial_accounts
        context['financial_documents'] = tag.financialdocument_set.all()
        context['transactions'] =tag.transaction_set.all()
        return render(request, TEMPLATE_ROOT+"tag.html", context)

class FinancialAccountViews(View):
    def financial_account(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['title'] = "HesabYar Ver 1.0.0"
        financial_account = FinancialAccountRepo(
            request=request).financial_account(*args, **kwargs)
        if financial_account is None:
            mv=MessageView(request=request)
            mv.title="دسترسی غیر مجاز برای شما"
            return mv.response()
        context['financial_account'] = financial_account
        financial_documents = FinancialDocumentRepo(request=request).list(
            account_id=financial_account.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentForAccountSerializer(financial_documents, many=True).data)
        context['financial_documents_s'] = financial_documents_s
        context['rest']=financial_account.rest()
        if request.user.has_perm(APP_NAME+".add_financialdocumet"):
            document_categories=FinancialDocumentCategoryRepo(request=request).list()
            context['document_categories']=document_categories
            context['add_financial_document_form'] = AddFinancialDocumentForm()
        return render(request, TEMPLATE_ROOT+"financial-account.html", context)

    def financial_account_print(self, request, *args, **kwargs):
        context = getContext(request=request)
        
        context['no_footer']=True
        context['no_nav_bar']=True
        context['title'] = "HesabYar Ver 1.0.0"
        financial_account = FinancialAccountRepo(
            request=request).financial_account(*args, **kwargs)
        context['financial_account'] = financial_account
        financial_documents = FinancialDocumentRepo(request=request).list(
            account_id=financial_account.id)
        context['financial_documents'] = financial_documents
        financial_documents_s = json.dumps(
            FinancialDocumentForAccountSerializer(financial_documents, many=True).data)
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


        ware_houses=WareHouseRepo(request=request).list().all()

        availables_list=[]
        
        for ware_house in ware_houses:
            line=warehouse_sheets.filter(product_id=product.id).filter(ware_house=ware_house).first()
            if line is not None:
                list_item={'product':{'id':product.pk,'title':product.title,'get_absolute_url':product.get_absolute_url()}}
                list_item['available']=line.available()
                list_item['unit_name']=line.unit_name
                list_item['ware_house']={'title':ware_house.title,'get_absolute_url':ware_house.get_absolute_url()}
                availables_list.append(list_item)
                context['availables_list']=json.dumps(availables_list)


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
        financial_account_id=kwargs['financial_account_id'] if 'financial_account_id' in kwargs else 0
        financial_account_repo=FinancialAccountRepo(request=request)
        if financial_account_id==0:
            financial_account=financial_account_repo.me
        else:
            financial_account=financial_account_repo.financial_account(*args, **kwargs)

        (sell_benefit,sell_loss,tax,sell_service,buy_service,ship_fee)=financial_account_repo.report(financial_account_id=financial_account.id,start_date=start_date,end_date=end_date)
        wage_repo=WageRepo(request=request)
        cost_repo=CostRepo(request=request)
        context['financial_account']=financial_account
        sell_benefit=sell_benefit
        sell_loss=sell_loss
        tax=tax
        ship_fee=ship_fee
        wages=wage_repo.wage_sum(financial_account=financial_account,start_date=start_date,end_date=end_date)
        costs=cost_repo.cost_sum(financial_account=financial_account,start_date=start_date,end_date=end_date)
        buy_service=buy_service
        sell_service_benefit=sell_service-buy_service
        rest=0
        rest+=sell_benefit 
        rest-=wages
        rest-=buy_service
        rest+=sell_service
        rest-=tax
        rest-=costs
        context['tax']=tax
        context['sell_service_benefit']=sell_service_benefit
        context['wages']=wages
        context['sell_benefit']=sell_benefit
        context['start_date']=start_date
        context['end_date']=end_date
        context['buy_service']=buy_service
        context['sell_service']=sell_service
        context['ship_fee']=ship_fee
        context['costs']=costs
        context['rest']=rest

        







        buy_=0
        sell_=0
        cost_internet=cost_repo.cost_sum(cost_type=CostTypeEnum.INTERNET,financial_account=financial_account,start_date=start_date,end_date=end_date)
        cost_gas=cost_repo.cost_sum(cost_type=CostTypeEnum.GAS,financial_account=financial_account,start_date=start_date,end_date=end_date)
        cost_water=cost_repo.cost_sum(cost_type=CostTypeEnum.WATER,financial_account=financial_account,start_date=start_date,end_date=end_date)
        cost_telephone=cost_repo.cost_sum(cost_type=CostTypeEnum.TELEPHONE,financial_account=financial_account,start_date=start_date,end_date=end_date)
        cost_electricity=cost_repo.cost_sum(cost_type=CostTypeEnum.ELECTRICITY,financial_account=financial_account,start_date=start_date,end_date=end_date)
        cost_transport=cost_repo.cost_sum(cost_type=CostTypeEnum.TRANSPORT,financial_account=financial_account,start_date=start_date,end_date=end_date)
        cost_rent=cost_repo.cost_sum(cost_type=CostTypeEnum.RENT,financial_account=financial_account,start_date=start_date,end_date=end_date)
        rest_=0
        rest_+=sell_
        rest_-=wages
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
    def costs(self,request,*args, **kwargs):
        context=getContext(request=request)
        costs=CostRepo(request=request).list(*args, **kwargs)
        context['costs']=costs
        return render(request,TEMPLATE_ROOT+"costs.html",context)

    def cost(self,request,*args, **kwargs):
        context=getContext(request=request)
        cost=CostRepo(request=request).cost(*args, **kwargs)
        context['cost']=cost
        context['transaction']=cost
        transaction=cost
        context.update(getTransactionContext(request=request,transaction=transaction))
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

class SpendViews(View):
    def spends(self,request,*args, **kwargs):
        context=getContext(request=request)
        spends=SpendRepo(request=request).list(*args, **kwargs)
        context['spends']=spends
        spends_s=json.dumps(SpendSerializer(spends,many=True).data)
        context['spends_s']=spends_s
        return render(request,TEMPLATE_ROOT+"spends.html",context)

class WageViews(View):
    def wage(self,request,*args, **kwargs):
        context=getContext(request=request)
        wage=WageRepo(request=request).wage(*args, **kwargs)
        context['wage']=wage
        context['transaction']=wage
        transaction=wage
        context.update(getTransactionContext(request=request,transaction=transaction))
        return render(request,TEMPLATE_ROOT+"wage.html",context)
    def wages(self,request,*args, **kwargs):
        context=getContext(request=request)
        wages=WageRepo(request=request).list(*args, **kwargs)
        context['wages']=wages
        return render(request,TEMPLATE_ROOT+"wages.html",context)


    def new_wage(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_accounts=FinancialAccountRepo(request=request).list(*args, **kwargs)
        context['payment_methods']=(u[0] for u in PaymentMethodEnum.choices)
        context['cost_types']=(u[0] for u in CostTypeEnum.choices)
        context['financial_accounts']=financial_accounts
        
        if request.user.has_perm(APP_NAME+".add_wage"):
            context['add_wage_form']=AddWageForm()
        return render(request,TEMPLATE_ROOT+"new-wage.html",context)



class WareHouseSheetViews(View):
    def ware_house_sheet(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouse_sheet=WareHouseSheetRepo(request=request).warehouse_sheet(*args, **kwargs)
        context['warehouse_sheet']=warehouse_sheet
        return render(request,TEMPLATE_ROOT+"ware-house-sheet.html",context)

 
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
        return redirect(invoice.get_edit_url2())


        
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
        context['no_footer']=True
        context['no_nav_bar']=True
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
        product_repo=ProductRepo(request=request)
        me=ProfileRepo(request=request).me
        for invoice_line in invoice_lines:
            product=product_repo.product(product_id=invoice_line.productorservice.id)
            if product is not None:
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
        transaction=invoice
        context.update(getTransactionContext(request=request,transaction=transaction))
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
        financial_document = FinancialDocumentRepo(request=request).financial_document(*args, **kwargs)
        context['financial_document'] = financial_document
        financial_document_=financial_document.financial_document_()
        context['financial_document_'] = financial_document_
        
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
        transaction=cheque
        context.update(getTransactionContext(request=request,transaction=transaction))
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
        transaction=payment
        context.update(getTransactionContext(request=request,transaction=transaction))
        return render(request,TEMPLATE_ROOT+"payment.html",context)
    
class TransactionViews(View):
    def transaction_category(self,request,*args, **kwargs):
        context=getContext(request=request)
        transaction_category=TransactionCategoryRepo(request=request).transaction_category(*args, **kwargs)
        if transaction_category is None:
            mv=MessageView(request=request)
            return mv.response(*args, **kwargs)
        transactions=transaction_category.transaction_set.all()
        context['transactions']=transactions
        context['page_pre_description']='دسته بندی'
        context['page_description']=transaction_category.title
        context['transactions_s']=json.dumps(TransactionSerializer(transactions,many=True).data)

        
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
    def transactions(self,request,*args, **kwargs):
        context=getContext(request=request)
        transactions=TransactionRepo(request=request).transactions(*args, **kwargs)
        context['transactions']=transactions
        context['transactions_s']=json.dumps(TransactionSerializer(transactions,many=True).data)

        
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
def getTransactionContext(request,transaction):
    context={}
    context['transaction']=transaction
    documents=transaction.documents.all()

    documents_s=json.dumps(DocumentSerializer(documents,many=True).data)
    context['documents']=documents
    context['documents_s']=documents_s
    if request.user.has_perm(APP_NAME+".change_transaction"):
        context['add_transaction_document_form']=AddTransactionDocumentForm()
    return context

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
    
    