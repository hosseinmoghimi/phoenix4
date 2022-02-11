from operator import inv
from django.utils import timezone
from urllib import request
from django import forms

from core.enums import UnitNameEnum
from hesabyar.enums import InvoiceStatusEnum, PaymentMethodEnum, TransactionStatusEnum
from .apps import APP_NAME
from .models import Cheque, FinancialAccount, FinancialDocument, FinancialDocumentCategory, FinancialYear, Invoice, InvoiceLine, Payment, Product, Service, Store, Tag, WareHouse, WareHouseSheet
from authentication.repo import ProfileRepo

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
        self.objects = FinancialDocument.objects.order_by('document_datetime')
        self.profile = ProfileRepo(user=self.user).me

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

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'tag_id' in kwargs:
            tag=TagRepo(request=self.request).tag(tag_id=kwargs['tag_id'])
            objects = tag.financialaccount_set.all()            
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def financial_account(self, *args, **kwargs):
        if 'financial_account_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_account_id']).first()
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
    def list(self):
        objects=self.objects
        return objects
    def ware_house(self, *args, **kwargs):
        if 'ware_house_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
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
        self.objects = WareHouseSheet.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'product_id' in kwargs:
            objects = objects.filter(product_id=kwargs['product_id'])
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

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
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
        if not self.user.has_perm(APP_NAME+".change_invoice"):
            return
        invoice=self.invoice(*args, **kwargs)
        if invoice is None:
            return

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
        print(invoice.payment_method)
        print(10*"#$$%")
        if invoice.payment_method==PaymentMethodEnum.CARD or invoice.payment_method==PaymentMethodEnum.POS:
            payment=Payment()
            payment.title="پرداخت برای "+invoice.title
            payment.pay_from=invoice.pay_to
            payment.pay_to=invoice.pay_from
            payment.creator=self.profile
            payment.amount=invoice.amount
            payment.transaction_datetime=invoice.transaction_datetime
            payment.payment_method=invoice.payment_method
            payment.save()
        # self.update_financial_documents(invoice)
        return invoice
    # def update_financial_documents(self,invoice,*args, **kwargs):
    #     financial_year=FinancialYear.get_by_date(date=invoice.invoice_datetime)
    #     FinancialDocumentCategory.objects.get_or_create(title="فروش")
    #     FinancialDocumentCategory.objects.get_or_create(title="پرداخت با کارتخوان")
    #     FinancialDocumentCategory.objects.get_or_create(title="پرداخت نقدی")

    #     if invoice.status==InvoiceStatusEnum.APPROVED:
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
        if not self.user.has_perm(APP_NAME+".add_invoice"):
            return
        invoice=Invoice()
        me_store=StoreRepo(request=self.request).me
        me_p=FinancialAccountRepo(request=self.request).me

        if 'pay_from_id' in kwargs:
            invoice.pay_from_id=kwargs['pay_from_id'] 
        else:
            invoice.pay_from_id=me_store.id

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
        invoice_line=InvoiceLine()
        invoice_line.invoice=invoice
        invoice_line.productorservice=Product.objects.first()
        invoice_line.quantity=7
        invoice_line.unit_price=18000
        invoice_line.unit_name=UnitNameEnum.ADAD
        invoice_line.row=1

        invoice_line.save()
        return invoice


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
        
