from rest_framework import serializers

from authentication.serializers import ProfileSerializer
from .models import FinancialDocument, FinancialAccount, FinancialDocumentCategory, Invoice, InvoiceLine, Product, ProductOrService, ProfileFinancialAccount, Store, WareHouse, WareHouseSheet


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




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'get_absolute_url','available',
                  'thumbnail']


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






class InvoiceFullSerializer(serializers.ModelSerializer):
    customer=ProfileFinancialAccountSerializer()
    seller=StoreSerializer()
    class Meta:
        model = Invoice
        fields = ['id','title','customer','seller','description','get_absolute_url','persian_invoice_datetime']


class InvoiceLineForProductOrServiceSerializer(serializers.ModelSerializer):
    invoice=InvoiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','invoice', 'quantity', 'unit_price',
                  'description']



class InvoiceLineSerializer(serializers.ModelSerializer):
    productorservice=ProductOrServiceSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','productorservice', 'quantity', 'unit_price',
                  'description']

