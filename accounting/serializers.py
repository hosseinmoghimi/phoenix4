from rest_framework import fields, serializers
from .models import Asset, BankAccount, FinancialAccount, Transaction
from authentication.serializers import ProfileSerializer

from market.models import Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields=['id','get_absolute_url']

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields=['id','title','get_edit_url','get_absolute_url']

class FinancialAccountSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = FinancialAccount
        fields=['id','profile','total','get_absolute_url']

class BankAccountSerializer(serializers.ModelSerializer):
    pay_to=FinancialAccountSerializer()
    pay_from=FinancialAccountSerializer()
    class Meta:
        model = BankAccount
        fields=['id','title','bank','branch','owner']


class TransactionSerializer(serializers.ModelSerializer):
    pay_to=FinancialAccountSerializer()
    pay_from=FinancialAccountSerializer()
    asset=AssetSerializer()
    order=OrderSerializer()
    class Meta:
        model = Transaction
        fields=['id','title','get_edit_url','description','asset','order','pay_to','pay_from','amount','persian_date_paid','rest','get_transaction2_url','get_icon','payment_method','get_color','get_absolute_url']
 