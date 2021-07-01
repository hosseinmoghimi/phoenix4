from rest_framework import fields, serializers
from .models import BankAccount, FinancialAccount, Transaction
from authentication.serilizers import ProfileSerializer
class FinancialAccountSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = FinancialAccount
        fields=['id','profile','total']

class BankAccountSerializer(serializers.ModelSerializer):
    pay_to=FinancialAccountSerializer()
    pay_from=FinancialAccountSerializer()
    class Meta:
        model = BankAccount
        fields=['id','title','bank','branch','owner']


class TransactionSerializer(serializers.ModelSerializer):
    pay_to=FinancialAccountSerializer()
    pay_from=FinancialAccountSerializer()
    class Meta:
        model = Transaction
        fields=['id','title','pay_to','pay_from','amount','persian_date_paid']