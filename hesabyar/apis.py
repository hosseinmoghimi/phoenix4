from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from .repo import FinancialDocumentRepo
from django.http import JsonResponse
from .forms import *
from .serializers import FinancialDocumentSerializer
class FoodApi(APIView):
    def add_food(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            add_food_form=AddForm(request.POST)
            if add_food_form.is_valid():
                fm=add_food_form.cleaned_data
                title=fm['title']
                financial_document=FinancialDocumentRepo(request=request).add_financial_document(title=title)
                if financial_document is not None:
                    context['financial_document']=FinancialDocumentSerializer(financial_document).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
