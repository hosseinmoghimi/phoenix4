from rest_framework import serializers
from .models import FinancialDocument, FinancialAccount, FinancialDocumentCategory, Invoice, InvoiceLine, Product, ProductOrService, WareHouse, WareHouseSheet


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

