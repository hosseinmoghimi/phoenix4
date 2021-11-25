from django.utils import timezone
from django.utils import translation
from resume.apps import APP_NAME
from accounting.models import Asset, AssetTransaction, BankAccount, FinancialAccount, MarketOrderTransaction, MoneyTransaction, ProjectTransaction, Transaction
from authentication.repo import ProfileRepo
from django.db.models import Q
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
        
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            return self.objects.filter(owner__profile_id=profile_id).filter(is_default=True).filter(is_active=True).first()
        if 'bank_account_id' in kwargs:
            pk=kwargs['bank_account_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        bank_account= self.objects.filter(pk=pk).first()
        return bank_account
    

       
class AssetRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Asset.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def asset(self,*args, **kwargs):
        pk=0
        
        if 'asset_id' in kwargs:
            pk=kwargs['asset_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        asset= self.objects.filter(pk=pk).first()
        return asset


       
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
        self.me=FinancialAccount.objects.filter(profile_id=self.profile.id).first()
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        return objects
    def financial_account(self,*args, **kwargs):
        pk=0
        
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            financial_account=self.objects.filter(profile_id=profile_id).first()
            if financial_account is None:
                financial_account=FinancialAccount(profile_id=profile_id)
                financial_account.save()
            return financial_account
        if 'financial_account_id' in kwargs:
            pk=kwargs['financial_account_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        financial_account= self.objects.filter(pk=pk).first()
        return financial_account 
       
class MoneyTransactionRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=MoneyTransaction.objects.order_by('date_paid')
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
            objects=objects.filter(Q(pay_to_id=financial_account_id)|Q(pay_from_id=financial_account_id))
        if 'pay_to_id' in kwargs and 'pay_from_id' in kwargs:
            pay_to_id=kwargs['pay_to_id']
            pay_from_id=kwargs['pay_from_id']
            objects1=objects.filter(pay_to_id=pay_to_id).filter(pay_from_id=pay_from_id)
            objects2=objects.filter(pay_from_id=pay_to_id).filter(pay_to_id=pay_from_id)
            list_id=[]
            list_final=[]
            for transaction in objects1:
                transaction.calculate_rest(*args, **kwargs) 
                list_id.append(transaction.pk)
                list_final.append(transaction)
            for transaction in objects2:
                transaction.calculate_rest(*args, **kwargs)
                list_id.append(transaction.pk)
                list_final.append(transaction)
            # return list_final 
            
            objects= self.objects.filter(id__in=list_id)
            for transaction in objects:
                transaction.calculate_rest(*args, **kwargs)
            return objects
            



        return objects
    def money_transaction(self,*args, **kwargs):
        pk=0
        
        if 'money_transaction_id' in kwargs:
            pk=kwargs['money_transaction_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        transaction= self.objects.filter(pk=pk).first()
        return transaction
    def add_transaction(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_transaction"):
            return
        asset_id=kwargs['asset_id'] if 'asset_id' in kwargs else None
        if asset_id is not None:
            #add AssetTransaction
            return
        transaction=MoneyTransaction()
        transaction.pay_to_id=kwargs['pay_to_id']
        transaction.pay_from_id=kwargs['pay_from_id']
        transaction.amount=kwargs['amount']
        transaction.paymet_method=kwargs['payment_method'] 
        transaction.title=kwargs['title']
        transaction.description=kwargs['description']
        date_paid=kwargs['date_paid'] if 'date_paid' in kwargs else None
        if date_paid is None:
            date_paid=timezone.now()
        transaction.date_paid=date_paid
        transaction.creator=self.profile
        transaction.class_name="moneytransaction"
        transaction.save()
        return transaction

 
class AssetTransactionRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=AssetTransaction.objects.order_by('date_paid')
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
            objects=objects.filter(Q(pay_to_id=financial_account_id)|Q(pay_from_id=financial_account_id))
        if 'pay_to_id' in kwargs and 'pay_from_id' in kwargs:
            pay_to_id=kwargs['pay_to_id']
            pay_from_id=kwargs['pay_from_id']
            objects1=objects.filter(pay_to_id=pay_to_id).filter(pay_from_id=pay_from_id)
            objects2=objects.filter(pay_from_id=pay_to_id).filter(pay_to_id=pay_from_id)
            list_id=[]
            list_final=[]
            for transaction in objects1:
                transaction.calculate_rest(*args, **kwargs) 
                list_id.append(transaction.pk)
                list_final.append(transaction)
            for transaction in objects2:
                transaction.calculate_rest(*args, **kwargs)
                list_id.append(transaction.pk)
                list_final.append(transaction)
            # return list_final 
            
            objects= self.objects.filter(id__in=list_id)
            for transaction in objects:
                transaction.calculate_rest(*args, **kwargs)
            return objects
            



        return objects
    def asset_transaction(self,*args, **kwargs):
        pk=0
        
        if 'asset_transaction_id' in kwargs:
            pk=kwargs['asset_transaction_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        transaction= self.objects.filter(pk=pk).first()
        return transaction
    def add_transaction(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_transaction"):
            return
        asset_id=kwargs['asset_id'] if 'asset_id' in kwargs else None
        if asset_id is not None:
            #add AssetTransaction
            return
        transaction=MoneyTransaction()
        transaction.pay_to_id=kwargs['pay_to_id']
        transaction.pay_from_id=kwargs['pay_from_id']
        transaction.amount=kwargs['amount']
        transaction.paymet_method=kwargs['payment_method'] 
        transaction.title=kwargs['title']
        transaction.description=kwargs['description']
        date_paid=kwargs['date_paid'] if 'date_paid' in kwargs else None
        if date_paid is None:
            date_paid=timezone.now()
        transaction.date_paid=date_paid
        transaction.creator=self.profile
        transaction.class_name="moneytransaction"
        transaction.save()
        return transaction

 
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
        self.objects=Transaction.objects.order_by('-date_paid')
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
            objects=objects.filter(Q(pay_to_id=financial_account_id)|Q(pay_from_id=financial_account_id))
        if 'pay_to_id' in kwargs and 'pay_from_id' in kwargs:
            pay_to_id=kwargs['pay_to_id']
            pay_from_id=kwargs['pay_from_id']
            objects1=objects.filter(pay_to_id=pay_to_id).filter(pay_from_id=pay_from_id)
            objects2=objects.filter(pay_from_id=pay_to_id).filter(pay_to_id=pay_from_id)
            list_id=[]
            list_final=[]
            for transaction in objects1:
                transaction.calculate_rest(*args, **kwargs) 
                list_id.append(transaction.pk)
                list_final.append(transaction)
            for transaction in objects2:
                transaction.calculate_rest(*args, **kwargs)
                list_id.append(transaction.pk)
                list_final.append(transaction)
            # return list_final 
            
            objects= self.objects.filter(id__in=list_id)
            for transaction in objects:
                transaction.calculate_rest(*args, **kwargs)
            return objects
            



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
        if not self.user.has_perm(APP_NAME+".add_transaction"):
            return
        asset_id=kwargs['asset_id'] if 'asset_id' in kwargs else None
        if asset_id is not None:
            #add AssetTransaction
            return
        print(kwargs)
        transaction=MoneyTransaction()
        transaction.pay_to_id=kwargs['pay_to_id']
        transaction.pay_from_id=kwargs['pay_from_id']
        transaction.amount=kwargs['amount']
        transaction.payment_method=kwargs['payment_method'] 
        transaction.title=kwargs['title']
        transaction.description=kwargs['description']
        date_paid=kwargs['date_paid'] if 'date_paid' in kwargs else None
        if date_paid is None:
            date_paid=timezone.now()
        transaction.date_paid=date_paid
        transaction.creator=self.profile
        transaction.class_name="moneytransaction"
        transaction.save()
        return transaction


 
class MarketOrderTransactionRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=MarketOrderTransaction.objects.order_by('date_paid')
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
            transaction=MarketOrderTransaction()
            transaction.pay_to_id=kwargs['pay_to_id']
            transaction.title=kwargs['title']
            transaction.pay_from_id=kwargs['pay_from_id']
            transaction.order_id=kwargs['order_id']
            transaction.amount=kwargs['amount']
            date_paid=kwargs['date_paid']
            if date_paid is None:
                date_paid=timezone.now()
            transaction.date_paid=date_paid
            transaction.creator=self.profile
            transaction.save()
            return transaction



class ProjectTransactionRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=ProjectTransaction.objects.order_by('date_paid')
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        


        return objects
    def project_transaction(self,*args, **kwargs):
        pk=0
        
        if 'project_transaction_id' in kwargs:
            pk=kwargs['project_transaction_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        transaction= self.objects.filter(pk=pk).first()
        return transaction
     