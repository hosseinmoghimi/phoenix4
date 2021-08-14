from authentication.repo import ProfileRepo
from rest_framework import serializers
from .models import Document, Payment, Stock
from authentication.serilizers import ProfileSerializer


class StockSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    agent=ProfileSerializer
    class Meta:
        model =Stock
        fields = ['id','profile','stock1','stock2','get_absolute_url','get_edit_url','get_stock_amount','agent']
class DocumentSerializer(serializers.ModelSerializer):
    stock=StockSerializer()
    class Meta:
        model =Document
        fields = ['id','stock','title','get_download_url','persian_date_added','get_image','get_edit_url']

class PaymentSerializer(serializers.ModelSerializer):
    stock=StockSerializer()
    class Meta:
        model =Payment
        fields = ['id','stock','title','image','payment_type','value','persian_date_paid','get_edit_url']
