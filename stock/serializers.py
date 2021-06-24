from authentication.repo import ProfileRepo
from rest_framework import serializers
from .models import Document, Stock
from authentication.serilizers import ProfileSerializer

class StockSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model =Stock
        fields = ['id','profile','stock1','stock2']
class DocumentSerializer(serializers.ModelSerializer):
    stock=StockSerializer()
    class Meta:
        model =Document
        fields = ['id','stock','title','get_download_url','persian_date_added','get_image','get_edit_url']
