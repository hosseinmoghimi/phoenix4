from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from .models import Cheque, FinancialDocument, FinancialAccount, FinancialDocumentCategory, Invoice, InvoiceLine, Payment, Product, ProductOrService, ProfileFinancialAccount, Service, Store, WareHouse, WareHouseSheet


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
        fields = ['id','persian_date_registered', 'ware_house','product','direction','status', 'get_absolute_url','quantity']




class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id','title','get_absolute_url','persian_invoice_datetime']
class ProfileFinancialAccountSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = ProfileFinancialAccount
        fields = ['id','profile','get_absolute_url']
class StoreSerializer(serializers.ModelSerializer):
    owner=ProfileFinancialAccountSerializer()
    class Meta:
        model = Store
        fields = ['id','owner','title','get_absolute_url']



class ChequeSerializer(serializers.ModelSerializer):
    owner=ProfileFinancialAccountSerializer()
    receiver=ProfileFinancialAccountSerializer()
    class Meta:
        model = Cheque
        fields = ['id','title','status','color','owner','receiver','description','amount','get_absolute_url','persian_cheque_date']




class InvoiceFullSerializer(serializers.ModelSerializer):
    customer=ProfileFinancialAccountSerializer()
    seller=StoreSerializer()
    class Meta:
        model = Invoice
        fields = ['id','title','payment_method','status','customer','seller','description','get_absolute_url','persian_invoice_datetime','ship_fee','discount','tax_percent']


class InvoiceLineForProductOrServiceSerializer(serializers.ModelSerializer):
    invoice=InvoiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','invoice', 'quantity', 'unit_price',
                  'description']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount','payment_method', 'title', 'persian_date_paid',
                  'description'
                  ]


class InvoiceLineSerializer(serializers.ModelSerializer):
    productorservice=ProductOrServiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','productorservice','unit_name', 'quantity', 'unit_price',
                  'description']

