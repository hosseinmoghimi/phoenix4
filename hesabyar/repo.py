from datetime import timedelta
from tracemalloc import start
from urllib import request
from django.db.models import Q
from authentication.repo import ProfileRepo
from core.enums import UnitNameEnum
from django.utils import timezone
from core.models import Document

from hesabyar.enums import CostTypeEnum, PaymentMethodEnum, SpendTypeEnum, TransactionStatusEnum
from utility.persian import PersianCalendar

from .apps import APP_NAME
from .models import (Bank, BankAccount, Cheque, Cost, FinancialAccount, FinancialBalance, FinancialDocument,
                     FinancialDocumentCategory, FinancialYear, Guarantee,
                     Invoice, InvoiceLine, Payment, Product, Service, Spend, Store, StorePrice,
                     Transaction, TransactionCategory,Tag, Wage, WareHouse, WareHouseSheet)

class BankAccountRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = BankAccount.objects.all()
        self.profile = ProfileRepo(user=self.user).me
        
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for)
        return objects

    def bank_account(self, *args, **kwargs):
        if 'bank_account_id' in kwargs:
            return self.objects.filter(pk= kwargs['bank_account_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()

class StorePriceRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = StorePrice.objects.all()
        self.profile = ProfileRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+".view_storeprice"):
            self.objects = StorePrice.objects.all()
        elif self.profile is not None:
            self.objects = StorePrice.objects.filter(Q(store__profile=self.profile))
        else:
            self.objects = StorePrice.objects.filter(pk__lte=0)


        
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for)
        if 'store_id' in kwargs:
            store_id=kwargs['store_id']
            objects = objects.filter(store_id=store_id)
        if 'productorservice_id' in kwargs:
            productorservice_id=kwargs['productorservice_id']
            objects = objects.filter(productorservice_id=productorservice_id)
        return objects
    def add(self,*args, **kwargs):
        store=StoreRepo(request=self.request).store(*args, **kwargs)
        
        if store is None :
            return

        sp=StorePrice(store=store)
        if 'productorservice_id' in kwargs:
            sp.productorservice_id=kwargs['productorservice_id']
        if 'sell_price' in kwargs:
            sp.sell_price=kwargs['sell_price']
        if 'buy_price' in kwargs:
            sp.buy_price=kwargs['buy_price']
        sp.save()
        return sp
   


class BankRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Bank.objects.all()
        self.profile = ProfileRepo(user=self.user).me
        
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for)
        return objects

    def bank(self, *args, **kwargs):
        if 'bank_id' in kwargs:
            return self.objects.filter(pk= kwargs['bank_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
class FinancialDocumentCategoryRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = FinancialDocumentCategory.objects.all()
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for)
        return objects

    def financial_document_category(self, *args, **kwargs):
        if 'financial_document_category_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_document_category_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
class FinancialYearRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = FinancialYear.objects.all()
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            objects = objects.filter(account_id=account_id) 
        return objects

    def financial_year(self, *args, **kwargs):
        if 'date' in kwargs:
            return self.objects.filter(start_date__lte=kwargs['date']).filter(end_date__gte=kwargs['date']).first()
           
        if 'financial_year_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_year_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
            
    # def current_year(self, *args, **kwargs):
    #     current_date=timezone.now()
    #     current_year_= self.objects.filter(year=year).first()
    #     if current_year_ is None:
    #         current_year_=FinancialYear()
    #         from utility.persian import PersianCalendar
    #         current_date=PersianCalendar().from_gregorian(current_date)
    #         current_year_.title="سال مالی "+str(current_date.year)
    #         current_year_.start_date=PersianCalendar().to_gregorian(str(current_date)+"/01/01")
    #         current_year_.start_date=PersianCalendar().to_gregorian(str(current_date)+"/12/29")
    #         current_year_.save()
    #         return current_year_

            
   
class FinancialDocumentRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile = ProfileRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+".view_financialdocument"):
            self.objects = FinancialDocument.objects.order_by('document_datetime')
        elif self.profile is not None:
            self.objects = FinancialDocument.objects.filter(account__profile=self.profile).order_by('document_datetime')
        else:
            self.objects = FinancialDocument.objects.filter(pk__lte=0).order_by('document_datetime')

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'category_id' in kwargs:
            objects = objects.filter(category_id=kwargs['category_id'])
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            objects = objects.filter(account_id=account_id) 
        return objects

    def financial_document(self, *args, **kwargs):
        if 'financial_document_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_document_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
            
    def add_financial_document(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_financialdocument"):
            return
        financial_document_=FinancialDocument()
        if 'document_datetime' in kwargs:
            financial_document_.document_datetime= kwargs['document_datetime']
        else:
            financial_document_.document_datetime= timezone.now()

        if 'financial_year_id' in kwargs:
            financial_document_.financial_year_id= kwargs['financial_year_id']
        else:
            financial_year= FinancialYearRepo(request=self.request).financial_year(date=financial_document_.document_datetime)
            financial_document_.financial_year_id= financial_year.id

        if 'account_id' in kwargs:
            financial_document_.account_id= kwargs['account_id']
        if 'title' in kwargs:
            financial_document_.title= kwargs['title']
        if 'bestankar' in kwargs:
            financial_document_.bestankar= kwargs['bestankar']
        if 'bedehkar' in kwargs:
            financial_document_.bedehkar= kwargs['bedehkar']
        if 'category_id' in kwargs:
            financial_document_.category_id= kwargs['category_id']
        financial_document_.save()
        return financial_document_



# class ProfileFinancialAccountRepo:
#     def __init__(self, *args, **kwargs):
#         self.request = None
#         self.user = None
#         if 'request' in kwargs:
#             self.request = kwargs['request']
#             self.user = self.request.user
#         if 'user' in kwargs:
#             self.user = kwargs['user']
#         self.objects = ProfileFinancialAccount.objects
#         self.profile = ProfileRepo(user=self.user).me
#         if self.profile is not None:
#             self.me=ProfileFinancialAccount.objects.filter(profile=self.profile).first()
#         else:
#             self.me=None

#     def list(self, *args, **kwargs):
#         objects = self.objects.all()
#         if 'for_home' in kwargs:
#             objects = objects.filter(for_home=kwargs['for_home'])
#         if 'search_for' in kwargs:
#             search_for=kwargs['search_for']
#             objects = objects.filter(title__contains=search_for) 
#         return objects

#     def profile_financial_account(self, *args, **kwargs):
#         if 'profile_financial_account_id' in kwargs:
#             return self.objects.filter(pk= kwargs['profile_financial_account_id']).first()
#         if 'pk' in kwargs:
#             return self.objects.filter(pk= kwargs['pk']).first()
#         if 'id' in kwargs:
#             return self.objects.filter(pk= kwargs['id']).first()
        

class FinancialAccountRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = FinancialAccount.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me=FinancialAccount.objects.filter(profile=self.profile).first()
        if self.user.has_perm(APP_NAME+".view_financialqaccount"):
            self.objects = FinancialAccount.objects.order_by('profile')
        elif self.profile is not None:
            self.objects = FinancialAccount.objects.filter(profile=self.profile).order_by('profile')
        else:
            self.objects = FinancialAccount.objects.filter(pk__lte=0).order_by('profile')

    def list(self, *args, **kwargs):
        if 'all' in kwargs and kwargs['all']==True:
            return FinancialAccount.objects.order_by("profile__user__last_name")
        objects = self.objects.all()
        if 'tag_id' in kwargs:
            tag=TagRepo(request=self.request).tag(tag_id=kwargs['tag_id'])
            objects = tag.financialaccount_set.all()            
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for) |Q(profile__user__first_name__contains=search_for)|Q(profile__user__last_name__contains=search_for))
        return objects

    def financial_account(self, *args, **kwargs):
        if 'financial_account_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_account_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        
    def report(self,financial_account_id,start_date,end_date):
        sell_benefit=0
        sell_loss=0
        tax=0
        sell_service=0
        buy_service=0
        ship_fee=0
        fds=FinancialDocumentRepo(request=self.request).list(account_id=financial_account_id).filter(document_datetime__lte=end_date).filter(document_datetime__gte=start_date)
        for fd in fds:
            for fb in fd.financialbalance_set.all():
                sell_benefit+=fb.sell_benefit
                sell_loss+=fb.sell_loss
                tax+=fb.tax
                sell_service+=fb.sell_service
                buy_service+=fb.buy_service
                ship_fee+=fb.ship_fee
        return (sell_benefit,sell_loss,tax,sell_service,buy_service,ship_fee)

    def report_year(self,*args, **kwargs):
        financial_account=self.financial_account(*args, **kwargs)
        year=int(kwargs['year'])
        month=int(kwargs['month'])
        if month>0 and month<13:
            if month<9:
                start_date=str(year)+"/0"+str(month)+"/01 00:00:00"
                end_date=str(year)+"/0"+str(month+1)+"/01 00:00:00"
            elif month==9:
                start_date=str(year)+"/09/01 00:00:00"
                end_date=str(year)+"/10/01 00:00:00"
            elif month==12:
                start_date=str(year)+"/12/01 00:00:00"
                end_date=str(year+1)+"/01/01 00:00:00"
            else:
                start_date=str(year)+"/"+str(month)+"/01 00:00:00"
                end_date=str(year)+"/"+str(month+1)+"/01 00:00:00"
            
        start_date=PersianCalendar().to_gregorian(start_date)
        end_date=PersianCalendar().to_gregorian(end_date)
        sell_benefit=0
        sell_loss=0
        tax=0
        sell_service=0
        buy_service=0
        ship_fee=0
        wage=0
        discount=0
        docs=FinancialBalance.objects.filter(financial_document__account=financial_account).filter(financial_document__document_datetime__lte=end_date).filter(financial_document__document_datetime__gte=start_date)
        for doc in docs:
            sell_benefit+=doc.sell_benefit        
            tax+=doc.tax        
            sell_loss+=doc.sell_loss        
            sell_service+=doc.sell_service        
            buy_service+=doc.buy_service        
            ship_fee+=doc.ship_fee        
            discount+=doc.discount        
        return (start_date,end_date,sell_benefit,sell_loss,tax,sell_service,buy_service,ship_fee,discount)

class TransactionCategoryRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = TransactionCategory.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def transaction_category(self, *args, **kwargs):
        if 'transaction_category_id' in kwargs:
            return self.objects.filter(pk= kwargs['transaction_category_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(title= kwargs['title']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        



class TagRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Tag.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def tag(self, *args, **kwargs):
        if 'tag_id' in kwargs:
            return self.objects.filter(pk= kwargs['tag_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        

class ServiceRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Service.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def service(self, *args, **kwargs):
        if 'service_id' in kwargs:
            return self.objects.filter(pk= kwargs['service_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        

class ProductRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Product.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def product(self, *args, **kwargs):
        if 'product_id' in kwargs:
            return self.objects.filter(pk= kwargs['product_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        
        


        
class WareHouseRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouse.objects

        if self.user.has_perm(APP_NAME+".view_warehouse"):
            self.objects = WareHouse.objects.order_by('title')
        elif self.profile is not None:
            self.objects = WareHouse.objects.filter(owner__profile=self.profile).order_by('title')
        else:
            self.objects = WareHouse.objects.filter(pk__lte=0).order_by('title')

    def list(self):
        objects=self.objects
        return objects
    def ware_house(self, *args, **kwargs):
        if 'ware_house_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'store_id' in kwargs:
            return self.objects.filter(store_id=kwargs['store_id']).first()
        if 'owner_id' in kwargs:
            return self.objects.filter(owner_id=kwargs['owner_id']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
            
class WareHouseSheetRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = WareHouseSheet.objects.order_by('-date_registered')
        self.profile = ProfileRepo(user=self.user).me

        if self.user.has_perm(APP_NAME+".view_warehousesheet"):
            self.objects = WareHouseSheet.objects.order_by('-date_registered')
        elif self.profile is not None:
            self.objects = WareHouseSheet.objects.filter(ware_house__owner__profile=self.profile).order_by('-date_registered')
            # self.objects = WareHouseSheet.objects.filter(pk__gte=0).order_by('-date_registered')
        else:
            self.objects = WareHouseSheet.objects.filter(pk__lte=0).order_by('-date_registered')

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'product_id' in kwargs:
            objects = objects.filter(product_id=kwargs['product_id'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'ware_house_id' in kwargs:
            objects = objects.filter(ware_house_id=kwargs['ware_house_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def warehouse_sheet(self, *args, **kwargs):
        if 'ware_house_sheet_id' in kwargs:
            return self.objects.filter(pk= kwargs['ware_house_sheet_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        if 'warehouse_sheet_id' in kwargs:
            return self.objects.filter(pk= kwargs['warehouse_sheet_id']).first()
        
    def change_state(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_warehousesheet"):
            return 
        warehouse_sheet=self.warehouse_sheet(*args, **kwargs) 
        print(warehouse_sheet)
        if 'status' in kwargs:
            status=kwargs['status']
            if warehouse_sheet is not None:
                warehouse_sheet.status=status
                warehouse_sheet.save()
                return warehouse_sheet
class InvoiceLineRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = InvoiceLine.objects
        self.profile = ProfileRepo(user=self.user).me

        if self.user.has_perm(APP_NAME+".view_invoiceline"):
            self.objects = InvoiceLine.objects.order_by('invoice__transaction_datetime')
        elif self.profile is not None:
            self.objects = InvoiceLine.objects.filter(Q(invoice__pay_from__profile=self.profile)|Q(invoice__pay_to__profile=self.profile)).order_by('invoice__transaction_datetime')
        else:
            self.objects = InvoiceLine.objects.filter(pk__lte=0).order_by('invoice__transaction_datetime')

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'product_id' in kwargs:
            objects = objects.filter(productorservice_id=kwargs['product_id'])
        if 'service_id' in kwargs:
            objects = objects.filter(productorservice_id=kwargs['service_id'])
        if 'ware_house_id' in kwargs:
            objects = objects.filter(ware_house_id=kwargs['ware_house_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def invoice_line(self, *args, **kwargs):
        if 'invoice_line_id' in kwargs:
            return self.objects.filter(pk= kwargs['invoice_line_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
       
class TransactionRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Transaction.objects.all().order_by('transaction_datetime')
        self.profile = ProfileRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+".view_transaction"):
            self.objects = self.objects
        elif self.profile is not None:
            self.objects = self.objects.filter(Q(pay_from__profile=self.profile)|Q(pay_to__profile=self.profile))
        else:
            self.objects = self.objects.filter(pk__lte=0)

    def transactions(self, *args, **kwargs):
        return self.list(*args, **kwargs)
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def transaction(self, *args, **kwargs):
        if 'transaction_id' in kwargs:
            return self.objects.filter(pk= kwargs['transaction_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
    def add_document(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_transaction"):
            return
        transaction=self.transaction(*args, **kwargs)
        if transaction is None:
                return
        is_open=False
        title=kwargs['title'] if 'title' in kwargs else "سند"
        file=kwargs['file']
        priority=kwargs['priority'] if 'priority' in kwargs else 100
        document=Document(icon_fa="fa fa-download",title=title,is_open=is_open,file=file,priority=priority,profile=self.profile)
        document.save()
        document.profiles.add(self.profile)
        transaction.documents.add(document)
        return document
     
class InvoiceRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Invoice.objects
        self.profile = ProfileRepo(user=self.user).me

        if self.user.has_perm(APP_NAME+".view_invoice"):
            self.objects = Invoice.objects.order_by('transaction_datetime')
        elif self.profile is not None:
            self.objects = Invoice.objects.filter(Q(pay_from__profile=self.profile)|Q(pay_to__profile=self.profile)).order_by('transaction_datetime')
        else:
            self.objects = Invoice.objects.filter(pk__lte=0).order_by('transaction_datetime')



    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def invoice(self, *args, **kwargs):
        if 'invoice_id' in kwargs:
            return self.objects.filter(pk= kwargs['invoice_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
    
    def edit_invoice(self,*args, **kwargs):
        invoice=self.invoice(*args, **kwargs)
        if invoice is None:
            return
        if self.user.has_perm(APP_NAME+".change_invoice"):
            pass
        elif invoice.pay_from.profile==self.profile:
            pass
        else:
            return
        if invoice.status==TransactionStatusEnum.DELIVERED:
            return None
        if invoice.status==TransactionStatusEnum.APPROVED:
            return None
        if 'title' in kwargs:
            invoice.title=kwargs['title']
        if 'pay_from_id' in kwargs:
            invoice.pay_from_id=kwargs['pay_from_id']

        if 'payment_method' in kwargs:
            invoice.payment_method=kwargs['payment_method']

        if 'status' in kwargs:
            invoice.status=kwargs['status']

        if 'pay_to_id' in kwargs:
            invoice.pay_to_id=kwargs['pay_to_id']

        if 'invoice_datetime' in kwargs:
            invoice.invoice_datetime=kwargs['invoice_datetime']
            invoice.transaction_datetime=kwargs['invoice_datetime']

        if 'description' in kwargs:
            invoice.description=kwargs['description']

        if 'discount' in kwargs:
            invoice.discount=kwargs['discount']

        if 'ship_fee' in kwargs:
            invoice.ship_fee=kwargs['ship_fee']

        if 'tax_percent' in kwargs:
            invoice.tax_percent=kwargs['tax_percent']

        invoice.save()
        if 'lines' in kwargs:
            invoice_lines=kwargs['lines']
            invoice.invoice_lines().delete()
            amount=0
            for line in invoice_lines:
                if int(line['quantity'])>0:
                    invoice_line=InvoiceLine()
                    invoice_line.invoice=invoice
                    invoice_line.productorservice_id=int(line['productorservice_id'])
                    invoice_line.quantity=int(line['quantity'])
                    invoice_line.row=int(line['row'])
                    invoice_line.unit_price=int(line['unit_price'])
                    invoice_line.unit_name=line['unit_name']
                    invoice_line.save()
                    amount1=invoice_line.unit_price*invoice_line.quantity
                    # print(amount1)
                    # print(10*"%$#@#$%^")
                    amount=amount+amount1
        tax_amount=int(0.01*invoice.tax_percent*(amount+invoice.ship_fee))
        invoice.amount=amount+invoice.ship_fee+tax_amount-invoice.discount
        invoice.tax_amount=tax_amount
        if invoice.title is None or invoice.title=="":
            invoice.title=f"فاکتور شماره {invoice.pk}"
        invoice.save()
        if (invoice.status==TransactionStatusEnum.APPROVED or invoice.status==TransactionStatusEnum.DELIVERED)and (invoice.payment_method==PaymentMethodEnum.CARD or invoice.payment_method==PaymentMethodEnum.POS):
            payment=Payment()
            payment.title="پرداخت برای "+invoice.title
            payment.pay_from=invoice.pay_to
            payment.pay_to=invoice.pay_from
            payment.creator=self.profile
            payment.amount=invoice.amount
            delta=timedelta(minutes=1)
            payment.transaction_datetime=invoice.transaction_datetime+delta
            payment.payment_method=invoice.payment_method
            payment.save()
        # self.update_financial_documents(invoice)
        if invoice.status==TransactionStatusEnum.DELIVERED:
            for invoice_line in invoice.invoice_lines():
                wh_sheet=WareHouseSheet()
                wh_sheet.invoice=invoice
                wh_sheet.product_id=invoice_line.productorservice.id
        fd=FinancialDocument.objects.filter(account=invoice.pay_from).filter(transaction=invoice).first()
        if fd is not None:
            fb=FinancialBalance(financial_document=fd)
            sell_benefit=0
            for line in invoice.invoiceline_set.all():
                sp=StorePrice.objects.filter(store_id=invoice.pay_from.id).filter(productorservice_id=line.productorservice.id).order_by('-date_added').first()
                if sp is not None:
                    sell_benefit+=line.quantity*(line.unit_price-sp.buy_price)
            fb.sell_benefit=sell_benefit
            fb.tax=invoice.tax_amount
            fb.discount=invoice.discount
            fb.ship_fee=invoice.ship_fee
            fb.save()
        return invoice
    # def update_financial_documents(self,invoice,*args, **kwargs):
    #     financial_year=FinancialYear.get_by_date(date=invoice.invoice_datetime)
    #     FinancialDocumentCategory.objects.get_or_create(title="فروش")
    #     FinancialDocumentCategory.objects.get_or_create(title="پرداخت با کارتخوان")
    #     FinancialDocumentCategory.objects.get_or_create(title="پرداخت نقدی")

    #     if invoice.status==TransactionStatusEnum.APPROVED:
    #         pass
    #     else:
    #         return
    #     category=FinancialDocumentCategory.objects.get(title="فروش")
    #     FinancialDocument.objects.filter(transaction=invoice).delete()

    #     ifd1=FinancialDocument()
    #     ifd1.financial_year=financial_year
    #     ifd1.category=category
    #     ifd1.account=invoice.customer
    #     ifd1.transaction=invoice
    #     ifd1.bedehkar=invoice.sum_total()
    #     ifd1.title=str(invoice)
    #     ifd1.document_datetime=invoice.invoice_datetime
    #     ifd1.save()

    #     ifd1=FinancialDocument()
    #     ifd1.bestankar=invoice.sum_total()
    #     ifd1.transaction=invoice
    #     ifd1.title=str(invoice)
    #     ifd1.financial_year=financial_year
    #     ifd1.category=category
    #     ifd1.document_datetime=invoice.invoice_datetime
    #     ifd1.account=invoice.seller
    #     ifd1.save()
          
    def add(self,*args, **kwargs):
        store=StoreRepo(request=self.request).me
        if self.user.has_perm(APP_NAME+".add_invoice"):
            pass
        elif 'store' in kwargs:
            store=kwargs['store']
        elif store is not None:
            pass
        else:
            return
        invoice=Invoice()
        me_p=FinancialAccountRepo(request=self.request).me

        if 'pay_from_id' in kwargs:
            invoice.pay_from_id=kwargs['pay_from_id'] 
        else:
            invoice.pay_from_id=store.id

        if 'pay_to_id' in kwargs:
            invoice.pay_to_id=kwargs['pay_to_id'] 
        else:
            invoice.pay_to_id=me_p.id

        if 'invoice_datetime' in kwargs:
            invoice.invoice_datetime=kwargs['invoice_datetime']
        else:
            invoice.invoice_datetime=timezone.now()

        if 'transaction_datetime' in kwargs:
            invoice.transaction_datetime=kwargs['transaction_datetime']
        else:
            invoice.transaction_datetime=timezone.now()
        invoice.creator=self.profile
        invoice.save()
        # invoice_line=InvoiceLine()
        # invoice_line.invoice=invoice
        # invoice_line.productorservice=Product.objects.first()
        # invoice_line.quantity=0
        # invoice_line.unit_price=0
        # invoice_line.unit_name=UnitNameEnum.ADAD
        # invoice_line.row=1

        # invoice_line.save()
        return invoice

class GuaranteeRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Guarantee.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def guarantee(self, *args, **kwargs):
        if 'guarantee_id' in kwargs:
            return self.objects.filter(pk= kwargs['guarantee_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()


class SpendRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Spend.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects
    def spend(self, *args, **kwargs):
        if 'spend_id' in kwargs:
            return self.objects.filter(pk= kwargs['spend_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
    
class CostRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Cost.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects
    def cost_sum(self,*args, **kwargs):

        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
        if 'financial_account' in kwargs:
            financial_account=kwargs['financial_account']
            financial_account_id=financial_account.id
        if 'end_date' in kwargs:
            end_date=kwargs['end_date']
        if 'start_date' in kwargs:
            start_date=kwargs['start_date']
        cost_type='all'
        if 'cost_type' in kwargs:
            cost_type=kwargs['cost_type']

        sum=0
        if cost_type=='all':
            costs=Cost.objects.filter(pay_from_id=financial_account_id).filter(transaction_datetime__gte=start_date).filter(transaction_datetime__lte=end_date)
        else:
            cost_acc=FinancialAccount.objects.filter(title=cost_type).first()
            if cost_acc is None:
                return 0
            costs=Cost.objects.filter(pay_from_id=financial_account_id).filter(transaction_datetime__gte=start_date).filter(transaction_datetime__lte=end_date).filter(pay_to=cost_acc)

        for cost in costs:
            sum+=cost.amount
        return sum
    def cost(self, *args, **kwargs):
        if 'cost_id' in kwargs:
            return self.objects.filter(pk= kwargs['cost_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
    def add_cost(self,*args, **kwargs):
        # return
        if not self.request.user.has_perm(APP_NAME+".add_cost"):
            return
        cost=Cost(spend_type=SpendTypeEnum.COST)
        cost.creator=self.profile
        cost_type=None
        if 'pay_from_id' in kwargs:
            cost.pay_from_id=kwargs['pay_from_id']
        if 'cost_type' in kwargs:
            cost_type=kwargs['cost_type']
            cost_acc=FinancialAccount.objects.filter(title=cost_type).first()
            if cost_acc is None:
                cost_acc=FinancialAccount(title=cost_type)
                cost_acc.save()
            cost.pay_to_id=cost_acc.id
            cost.cost_type=cost_type
        if 'title' in kwargs:
            cost.title=kwargs['title']

        if 'description' in kwargs:
            cost.description=kwargs['description']
        if 'pay_to_id' in kwargs:
            cost.pay_to_id=kwargs['pay_to_id']
        if 'amount' in kwargs:
            cost.amount=kwargs['amount']
        if 'payment_method' in kwargs:
            cost.payment_method=kwargs['payment_method']

        if 'transaction_datetime' in kwargs:
            cost.transaction_datetime=kwargs['transaction_datetime']
        else:
            cost.transaction_datetime=timezone.now()
        if 'financial_year_id' in kwargs:
            cost.financial_year_id=kwargs['financial_year_id']
        else:
            cost.financial_year_id=FinancialYear.get_by_date(date=cost.transaction_datetime).id

        cost.save()
        return cost

class WageRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Wage.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects
    def wage_sum(self,*args, **kwargs):

        if 'financial_account' in kwargs:
            financial_account=kwargs['financial_account']
            financial_account_id=financial_account.id
        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
        if 'end_date' in kwargs:
            end_date=kwargs['end_date']
        if 'start_date' in kwargs:
            start_date=kwargs['start_date']

        sum=0
        wages=Wage.objects.filter(pay_from_id=financial_account_id).filter(transaction_datetime__gte=start_date).filter(transaction_datetime__lte=end_date)
        
        for wage in wages:
            sum+=wage.amount
        return sum
    def wage(self, *args, **kwargs):
        if 'wage_id' in kwargs:
            return self.objects.filter(pk= kwargs['wage_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
    def add_wage(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_wage"):
            return
        wage=Wage(spend_type=SpendTypeEnum.WAGE)
        wage.creator=self.profile
        if 'pay_from_id' in kwargs:
            wage.pay_from_id=kwargs['pay_from_id']
        if 'title' in kwargs:
            wage.title=kwargs['title']

        if 'description' in kwargs:
            wage.description=kwargs['description']
        if 'pay_to_id' in kwargs:
            wage.pay_to_id=kwargs['pay_to_id']
        if 'amount' in kwargs:
            wage.amount=kwargs['amount']
        if 'month' in kwargs and 'year' in kwargs:
            wage.month=kwargs['month']
            wage.year=kwargs['year']
        else:
            from utility.persian import PersianCalendar
            datattt=PersianCalendar().from_gregorian(kwargs['transaction_datetime'])
            year=(datattt[0:4])
            month=(datattt[5:7])
            month=int(month)
            year=int(year)
            wage.month=month
            wage.year=year
        if 'payment_method' in kwargs:
            wage.payment_method=kwargs['payment_method']

        if 'transaction_datetime' in kwargs:
            wage.transaction_datetime=kwargs['transaction_datetime']
        else:
            wage.transaction_datetime=timezone.now()
        if 'financial_year_id' in kwargs:
            wage.financial_year_id=kwargs['financial_year_id']
        else:
            wage.financial_year_id=FinancialYear.get_by_date(date=wage.transaction_datetime).id

        wage.save()

        # payment=Payment()
        # payment.pay_from=wage.pay_to
        # payment.pay_to=wage.pay_from
        # payment.transaction_datetime=wage.transaction_datetime
        # payment.amount=wage.amount
        # payment.creator=self.profile
        # payment.title="کارکرد حقوق "+wage.month_year()
        # payment.save()

        return wage

class StoreRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Store.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def store(self, *args, **kwargs):
        if 'store_id' in kwargs:
            return self.objects.filter(pk= kwargs['store_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()


class ChequeRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Cheque.objects
        self.profile = ProfileRepo(user=self.user).me
        pfa=FinancialAccountRepo(request=self.request).me
        if pfa is not None:
            self.me=Store.objects.filter(profile=self.profile).first()
        else:
            self.me=None
    def add_cheque(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_cheque"):
            return
        cheque=Cheque()
        me_acc=FinancialAccountRepo(request=self.request).me

        if 'title' in kwargs:
            cheque.title=kwargs['title']
        if 'cheque_date' in kwargs:
            cheque.cheque_date=kwargs['cheque_date']
        else:
            cheque.cheque_date=timezone.now()


            
        if 'pay_to_id' in kwargs:
            cheque.pay_to_id=kwargs['pay_to_id']
        else:
            cheque.pay_to_id=me_acc.id
        if 'pay_from_id' in kwargs:
            cheque.pay_from_id=kwargs['pay_from_id']
        else:
            cheque.pay_from_id=me_acc.id


        cheque.creator=self.profile


        if 'transaction_datetime' in kwargs:
            cheque.transaction_datetime=kwargs['transaction_datetime']
        else:
            cheque.transaction_datetime=timezone.now()
            
        if 'amount' in kwargs:
            cheque.amount=kwargs['amount']
        else:
            cheque.amount=0


        cheque.save()
        return cheque

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def cheque(self, *args, **kwargs):
        if 'cheque_id' in kwargs:
            return self.objects.filter(pk= kwargs['cheque_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        
class PaymentRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Payment.objects
        self.profile = ProfileRepo(user=self.user).me
        pfa=FinancialAccountRepo(request=self.request).me
        if pfa is not None:
            self.me=Store.objects.filter(profile=self.profile).first()
        else:
            self.me=None
    def add_payment(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_payment"):
            return
        payment=Payment()
        payment.creator=self.profile
        if 'title' in kwargs:
            payment.title=kwargs['title']

        if 'pay_from_id' in kwargs:
            payment.pay_from_id=kwargs['pay_from_id']
        if 'description' in kwargs:
            payment.description=kwargs['description']
        if 'pay_to_id' in kwargs:
            payment.pay_to_id=kwargs['pay_to_id']
        if 'amount' in kwargs:
            payment.amount=kwargs['amount']
        if 'payment_method' in kwargs:
            payment.payment_method=kwargs['payment_method']

        if 'transaction_datetime' in kwargs:
            payment.transaction_datetime=kwargs['transaction_datetime']
        else:
            payment.transaction_datetime=timezone.now()
        if 'financial_year_id' in kwargs:
            payment.financial_year_id=kwargs['financial_year_id']
        else:
            payment.financial_year_id=FinancialYear.get_by_date(date=payment.transaction_datetime).id

        payment.save()
        return payment

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def payment(self, *args, **kwargs):
        if 'payment_id' in kwargs:
            return self.objects.filter(pk= kwargs['payment_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        
