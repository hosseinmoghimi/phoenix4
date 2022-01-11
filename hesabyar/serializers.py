from rest_framework import serializers
from .models import FinancialDocument
class FinancialDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=FinancialDocument
        fields=['id','title','get_absolute_url']