from django.utils import timezone
from django.utils import translation
from resume.apps import APP_NAME
from accounting.models import BankAccount, FinancialAccount, Transaction
from authentication.repo import ProfileRepo

class BankAccountRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=BankAccount.objects.all()
    def bank_account(self,*args, **kwargs):
        pk=0
        
        if 'bank_account_id' in kwargs:
            pk=kwargs['bank_account_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        bank_account= self.objects.filter(pk=pk).first()
        return bank_account

       
class FinancialAccountRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=FinancialAccount.objects.all()
    def financial_account(self,*args, **kwargs):
        pk=0
        
        if 'financial_account_id' in kwargs:
            pk=kwargs['financial_account_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        financial_account= self.objects.filter(pk=pk).first()
        return financial_account

       
class TransactionRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Transaction.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def transaction(self,*args, **kwargs):
        pk=0
        
        if 'transaction_id' in kwargs:
            pk=kwargs['transaction_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        transaction= self.objects.filter(pk=pk).first()
        return transaction
    def add_transaction(self,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".add_transaction"):
            transaction=Transaction()
            transaction.pay_to_id=kwargs['pay_to']
            transaction.pay_from_id=kwargs['pay_from']
            transaction.amount=kwargs['amount']
            date_paid=kwargs['date_paid']
            if date_paid is None:
                date_paid=timezone.now()
            transaction.date_paid=date_paid
            transaction.creator=self.profile
            transaction.save()
            return transaction