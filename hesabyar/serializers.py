from rest_framework import serializers
from .models import FinancialDocument, FinancialAccount, FinancialDocumentCategory, InvoiceLine, Product


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





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'get_absolute_url',
                  'thumbnail']



class InvoiceLineSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model = InvoiceLine
        fields = ['id', 'row','product', 'quantity', 'unit_price',
                  'description']

