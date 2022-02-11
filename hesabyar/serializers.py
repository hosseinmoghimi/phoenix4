from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from .models import Cheque, FinancialDocument, FinancialAccount, FinancialDocumentCategory, Invoice, InvoiceLine, Payment, Product, ProductOrService, Service, Store, WareHouse, WareHouseSheet


class FinancialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = ['id', 'title', 'get_absolute_url']



class FinancialDocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDocumentCategory
        fields = ['id', 'title','color', 'get_absolute_url']

class FinancialDocumentSerializer(serializers.ModelSerializer):
    account = FinancialAccountSerializer()
    category = FinancialDocumentCategorySerializer()

    class Meta:
        model = FinancialDocument
        fields = ['id', 'title', 'account', 'get_absolute_url', 'bedehkar',
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


class WareHouseSheetSerializer(serializers.ModelSerializer):
    ware_house=WareHouseSerializer()
    product=ProductSerializer()
    class Meta:
        model = WareHouseSheet
        fields = ['id','persian_date_registered','unit_name','color', 'ware_house','product','direction','status', 'get_absolute_url','quantity']




class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','title','get_absolute_url','persian_invoice_datetime']
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


class InvoiceLineSerializer(serializers.ModelSerializer):
    productorservice=ProductOrServiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','productorservice','unit_name', 'quantity', 'unit_price',
                  'description']

