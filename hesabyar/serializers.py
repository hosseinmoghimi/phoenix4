from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from .models import Cheque, Cost, FinancialDocument, FinancialAccount, FinancialDocumentCategory, Guarantee, Invoice, InvoiceLine, Payment, Product, ProductOrService, Service, Spend, Store, Transaction, TransactionCategory, Wage, WareHouse, WareHouseSheet


class FinancialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = ['id', 'title', 'get_absolute_url']



class FinancialDocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDocumentCategory
        fields = ['id', 'title','color', 'get_absolute_url']
class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['id', 'title','color', 'get_absolute_url']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'title','category', 'get_absolute_url']

class FinancialDocumentSerializer(serializers.ModelSerializer):
    account = FinancialAccountSerializer()
    category = FinancialDocumentCategorySerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title','transaction','get_state_badge', 'account', 'get_absolute_url', 'bedehkar',
                  'bestankar', 'persian_document_datetime', 'category']



class FinancialDocumentForAccountSerializer(serializers.ModelSerializer):
    account = FinancialAccountSerializer()
    category = FinancialDocumentCategorySerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title','get_state_badge', 'rest','account', 'get_absolute_url', 'bedehkar',
                  'bestankar', 'persian_document_datetime', 'category']



class ProductOrServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrService
        fields = ['id', 'title', 'get_absolute_url',
                  'thumbnail']


class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = ['id', 'title', 'get_absolute_url',
                  'thumbnail']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'get_absolute_url','unit_price','unit_name','thumbnail']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'get_absolute_url','available','unit_price','unit_name','thumbnail']

class InvoiceBriefSerializer(serializers.ModelSerializer):
      class Meta:
        model = Invoice
        fields = ['id','title','get_absolute_url']

class ProductBriefSerializer(serializers.ModelSerializer):
      class Meta:
        model = Product
        fields = ['id','title','get_absolute_url']

class WareHouseSheetSerializer(serializers.ModelSerializer):
    ware_house=WareHouseSerializer()
    product=ProductSerializer()
    invoice=InvoiceBriefSerializer()
    class Meta:
        model = WareHouseSheet
        fields = ['id','available','persian_date_registered','invoice','unit_name','color', 'ware_house','product','direction','status', 'get_absolute_url','quantity','get_edit_url']




class GuaranteeSerializer(serializers.ModelSerializer):
    invoice=InvoiceBriefSerializer()
    product=ProductBriefSerializer()
    class Meta:
        model = Guarantee
        fields = ['id', 'invoice','product','type','get_edit_url','status','serial_no','persian_start_date','persian_end_date', 'get_absolute_url']


class InvoiceSerializer(serializers.ModelSerializer):
    pay_from=FinancialAccountSerializer()
    pay_to=FinancialAccountSerializer()
    class Meta:
        model = Invoice
        fields = ['id','title','pay_from','pay_to','get_absolute_url','persian_invoice_datetime']
class StoreSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Store
        fields = ['id','profile','title','get_absolute_url']



class ChequeSerializer(serializers.ModelSerializer):
    pay_to=FinancialAccountSerializer()
    pay_from=FinancialAccountSerializer()
    class Meta:
        model = Cheque
        fields = ['id','title','status','color','pay_to','pay_from','description','amount','get_absolute_url','persian_cheque_date']




class InvoiceFullSerializer(serializers.ModelSerializer):
    pay_to=FinancialAccountSerializer()
    pay_from=FinancialAccountSerializer()
    class Meta:
        model = Invoice
        fields = ['id','title','payment_method','status','pay_to','pay_from','description','get_absolute_url','persian_invoice_datetime','ship_fee','discount','tax_percent']


class InvoiceLineForProductOrServiceSerializer(serializers.ModelSerializer):
    invoice=InvoiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','invoice', 'quantity', 'unit_price','unit_name',
                  'description']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount','payment_method', 'title', 'persian_transaction_datetime',
                  'description'
                  ]


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = ['id', 'amount','payment_method', 'title', 'persian_transaction_datetime',
                  'description'
                  ]
class WageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wage
        fields = ['id', 'amount','payment_method', 'title', 'persian_transaction_datetime',
                  'description'
                  ]

class SpendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spend
        fields = ['id', 'amount','payment_method', 'title', 'persian_transaction_datetime',
                  'description'
                  ]

class InvoiceLineSerializer(serializers.ModelSerializer):
    productorservice=ProductOrServiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','productorservice','unit_name', 'quantity', 'unit_price',
                  'description']

