from accounting.models import FinancialAccount
from accounting.repo import FinancialAccountRepo, TransactionRepo
from django.shortcuts import render
from .apps import APP_NAME
from django.views import View
from core.views import CoreContext

TEMPLATE_ROOT=APP_NAME+"/"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context



class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        transactions=TransactionRepo(request=request).list()
        context['transactions']=transactions
        return render(request,TEMPLATE_ROOT+"index.html",context)
class TransactionViews(View):
    def transaction(self,request,*args, **kwargs):
        context=getContext(request=request)
        transaction=TransactionRepo(request=request).transaction(*args, **kwargs)
        context['transaction']=transaction
        return render(request,TEMPLATE_ROOT+"transaction.html",context)
    def financial_account(self,request,*args, **kwargs):
        context=getContext(request=request)
        financial_account=FinancialAccountRepo(request=request).financial_account(*args, **kwargs)
        context['financial_account']=financial_account
        return render(request,TEMPLATE_ROOT+"financial-account.html",context)