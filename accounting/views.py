from accounting.serializers import FinancialAccountSerializer
from core.enums import ParametersEnum
from core.repo import ParameterRepo
from django.utils import translation
from accounting.models import FinancialAccount
from accounting.repo import AssetRepo, FinancialAccountRepo, TransactionRepo
from django.shortcuts import render,reverse
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext
import json
TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    parameter_repo = ParameterRepo(app_name=APP_NAME)
    context['layout_parent']="phoenix/layout.html"
    context['app']={
        'home_url': reverse(APP_NAME+":home"),
        'tel': parameter_repo.get(ParametersEnum.TEL).value,
        'title': parameter_repo.get(ParametersEnum.TITLE).value,
    }
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
        accounts=FinancialAccountRepo(request=request).list()
        context['accounts']=accounts
        assets=AssetRepo(request=request).list()
        context['assets']=assets
        financial_accounts=FinancialAccountRepo(request=request).list()
        financial_accounts_s=json.dumps(FinancialAccountSerializer(financial_accounts,many=True).data)
        context['financial_accounts_s']=financial_accounts_s
        return render(request,TEMPLATE_ROOT+"index.html",context)

class TransactionViews(View):
    def transactions(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_account=None
        financial_account_id=0
        if 'financial_account_id' in kwargs:
            financial_account_id=kwargs['financial_account_id']
            financial_account=FinancialAccountRepo(request=request).financial_account(financial_account_id=financial_account_id)
        transactions=TransactionRepo(request=request).list(*args, **kwargs)
        context['transactions']=transactions
        total=0
        for transaction in transactions:
            if transaction.pay_to_id==financial_account_id:
                total-=transaction.amount
            if transaction.pay_from_id==financial_account_id:
                total+=transaction.amount
        context['total']=total
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
        total=0
        # for transaction in transactions:
        #     if transaction.pay_to_id==financial_account_id:
        #         total-=transaction.amount
        #     if transaction.pay_from_id==financial_account_id:
        #         total+=transaction.amount
        context['total']=total
        return render(request,TEMPLATE_ROOT+"transactions.html",context)
    
    def transaction(self,request,*args, **kwargs):
        context=getContext(request=request)
        transaction=TransactionRepo(request=request).transaction(*args, **kwargs)
        context['transaction']=transaction
        return render(request,TEMPLATE_ROOT+"transaction.html",context)
    def financial_account(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_account=FinancialAccountRepo(request=request).financial_account(*args, **kwargs)
        context['financial_account']=financial_account
        context['transactions']=financial_account.transactions()
        context['transactions']=TransactionRepo(request=request).list(*args, **kwargs)
        
        return render(request,TEMPLATE_ROOT+"financial-account.html",context)