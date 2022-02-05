from pydoc import doc
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView

from utility.persian import PersianCalendar
from .repo import FinancialDocumentRepo
from django.http import JsonResponse
from .forms import *
from .serializers import FinancialDocumentSerializer
class BasicApi(APIView):
    def add_financial_document(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            add_financial_document_form=AddFinancialDocumentForm(request.POST)



            
            if add_financial_document_form.is_valid():
                log=3
                fm=add_financial_document_form.cleaned_data
                title=fm['title']
                bestankar=fm['bestankar']
                bedehkar=fm['bedehkar']
                document_datetime=fm['document_datetime']
                account_id=fm['account_id']
                category_id=fm['category_id']
                document_datetime=PersianCalendar().to_gregorian(document_datetime)
                financial_document=FinancialDocumentRepo(request=request).add_financial_document(
                    title=title,
                    bestankar=bestankar,
                    account_id=account_id,
                    bedehkar=bedehkar,
                    document_datetime=document_datetime,
                    category_id=category_id,
                )
                if financial_document is not None:
                    context['rest']=financial_document.account.rest()
                    context['financial_document']=FinancialDocumentSerializer(financial_document).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
