from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from .repo import CryptoTokenRepo
from django.http import JsonResponse
from .forms import *
from .serializers import CryptoTokenSerializer
class CryptoTokenApi(APIView):
    def add_crypto_token(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            add_crypto_token_form=AddCryptoTokenForm(request.POST)
            if add_crypto_token_form.is_valid():
                fm=add_crypto_token_form.cleaned_data
                title=fm['title']
                crypto_token=CryptoTokenRepo(request=request).add_crypto_token(title=title)
                if crypto_token is not None:
                    context['crypto_token']=CryptoTokenSerializer(crypto_token).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
