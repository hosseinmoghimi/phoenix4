from accounting.enums import PaymetMethodEnum
from accounting.serializers import FinancialAccountSerializer, TransactionSerializer
from core.enums import ParametersEnum
from core.forms import AddPageImageForm
from core.repo import ParameterRepo
from django.utils import translation
from accounting.models import FinancialAccount
from accounting.repo import AssetRepo, AssetTransactionRepo,ProjectTransactionRepo, FinancialAccountRepo, MoneyTransactionRepo, TransactionRepo
from django.shortcuts import render,reverse
from core.views import PageContext
from core.serializers import ImageSerializer
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext
import json
TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']="phoenix/layout.html"
     
    return context

class AssetViews(View):
    def asset(self,request,*args, **kwargs):
        context=getContext(request=request)
        asset=AssetRepo(request=request).asset()
        context['asset']=asset
        return render(request,TEMPLATE_ROOT+"asset.html",context)



class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)


        financial_accounts=FinancialAccountRepo(request=request).list()
        context['financial_accounts']=financial_accounts
        context['financial_accounts_s']=json.dumps(FinancialAccountSerializer(financial_accounts,many=True).data)


        assets=AssetRepo(request=request).list()
        context['assets']=assets
        context.update(TransactionViews().get_add_transaction_context(request))

        # transactions=TransactionRepo(request=request).list()
        # context['transactions']=transactions
        # transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        # context['transactions_s']=transactions_s
        
        
        return render(request,TEMPLATE_ROOT+"index.html",context)

class TransactionViews(View):
    def get_add_transaction_context(self,request,*args, **kwargs):
        context={}
        payment_methods=(i[0] for i in PaymetMethodEnum.choices)
        context['payment_methods']=payment_methods
        financial_accounts=FinancialAccountRepo(request=request).list()
        financial_accounts_s=json.dumps(FinancialAccountSerializer(financial_accounts,many=True).data)
        context['financial_accounts_s']=financial_accounts_s
        return context
    def transactions(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_account=None
        financial_account_id=0
        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
            financial_account=FinancialAccountRepo(request=request).financial_account(financial_account_id=financial_account_id)
        transactions=TransactionRepo(request=request).list(*args, **kwargs)
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s
        total=0
        for transaction in transactions:
            if transaction.pay_to_id==financial_account_id:
                total-=transaction.amount
            if transaction.pay_from_id==financial_account_id:
                total+=transaction.amount
        context['total']=total
        context['rest']=total
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
    
    def transactions2(self,request,*args, **kwargs):
        context=getContext(request=request)
        # financial_account=None
        # pay_from_id=0
        # pay_to_id=0
        # if 'pay_from_id' in kwargs:
        #     pay_from_id=kwargs['pay_from_id']
        # if 'pay_to_id' in kwargs:
        #     pay_to_id=kwargs['pay_to_id']
        # financial_account=FinancialAccountRepo(request=request).financial_account(financial_account_id=financial_account_id)
        transactions=TransactionRepo(request=request).list(*args, **kwargs)
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s
        
        total=0
        # for transaction in transactions:
        #     if transaction.pay_to_id==financial_account_id:
        #         total-=transaction.amount
        #     if transaction.pay_from_id==financial_account_id:
        #         total+=transaction.amount
        if len(transactions)>0:
            tra=transactions.order_by('date_paid').last()
            tra.calculate_rest(pay_to_id=kwargs['pay_to_id'],pay_from_id=kwargs['pay_from_id'])
            total=tra.rest
        context['total']=total
        
        context['rest']=total
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
    
    def getTransactionContext(self,request,*args, **kwargs):
        transaction=TransactionRepo(request=request).transaction(*args, **kwargs)
        context=PageContext(request=request,page=transaction)
        transaction=transaction.get_sub_transaction()
        context['transaction']=transaction
        images=transaction.images()
        context['images_s']=json.dumps(ImageSerializer(images,many=True).data)

        if request.user.has_perm(APP_NAME+".add_pageimage"):
            context['add_page_image_form'] = AddPageImageForm()
        return context
    
    def transaction(self,request,*args, **kwargs):
        context=getContext(request=request)

        context.update(self.getTransactionContext(request,*args, **kwargs))
        return render(request,TEMPLATE_ROOT+"transaction.html",context)
    
    def money_transaction(self,request,*args, **kwargs):
        context=getContext(request=request)

        context.update(self.getTransactionContext(request,*args, **kwargs))
        # transaction=TransactionRepo(request=request).transaction(*args, **kwargs)
        # transaction=transaction.get_sub_transaction()
        # context['transaction']=transaction
        money_transaction=MoneyTransactionRepo(request=request).money_transaction(*args, **kwargs)
        context['money_transaction']=money_transaction
        return render(request,TEMPLATE_ROOT+"money-transaction.html",context)
    
    def project_transaction(self,request,*args, **kwargs):
        context=getContext(request=request)

        context.update(self.getTransactionContext(request,*args, **kwargs))
        
        project_transaction=ProjectTransactionRepo(request=request).project_transaction(*args, **kwargs)
        context['project_transaction']=project_transaction
        return render(request,TEMPLATE_ROOT+"project-transaction.html",context)
    
    def asset_transaction(self,request,*args, **kwargs):
        context=getContext(request=request)

        context.update(self.getTransactionContext(request,*args, **kwargs))
        asset_transaction=AssetTransactionRepo(request=request).asset_transaction(*args, **kwargs)
        context['asset_transaction']=asset_transaction
        return render(request,TEMPLATE_ROOT+"asset-transaction.html",context)
    
    def market_order_transaction(self,request,*args, **kwargs):
        context=getContext(request=request)

        context.update(self.getTransactionContext(request,*args, **kwargs))
        return render(request,TEMPLATE_ROOT+"transaction.html",context)
 
class FinancialAccountViews(View):   
    def financial_account(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_account=FinancialAccountRepo(request=request).financial_account(*args, **kwargs)
        context['financial_account']=financial_account
        transactions=TransactionRepo(request=request).list(financial_account_id=financial_account.id)
        context['transactions']=transactions
        transactions_s=json.dumps(TransactionSerializer(transactions,many=True).data)
        context['transactions_s']=transactions_s
        context['me_financial_account']=FinancialAccountRepo(request=request).me

        context['rest']=financial_account.total()
        
        context['transactions']=TransactionRepo(request=request).list(*args, **kwargs)
        
        context.update(TransactionViews().get_add_transaction_context(request))
        return render(request,TEMPLATE_ROOT+"financial-account.html",context)
    def financial_accounts(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_accounts=FinancialAccountRepo(request=request).list(*args, **kwargs)
        context['financial_accounts']=financial_accounts
        context['financial_accounts_s']=json.dumps(FinancialAccountSerializer(financial_accounts,many=True).data)
 
        
        return render(request,TEMPLATE_ROOT+"financial-accounts.html",context)