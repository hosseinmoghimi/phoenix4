import json
from django.shortcuts import render
from .forms import *
from .serializers import CryptoTokenSerializer
from .repo import CryptoTokenRepo
from .apps import APP_NAME
from core.views import CoreContext, PageContext
from django.views import View
TEMPLATE_ROOT="crypto/"
LAYOUT_PARENT="material-kit-pro/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['layout_parent']=LAYOUT_PARENT
    return context
# Create your views here.
class BasicView(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request=request)
        crypto_tokens=CryptoTokenRepo(request=request).list(*args, **kwargs)
        if request.user.has_perm(APP_NAME+".add_crypto_token"):
            context['add_crypto_token_form']=AddCryptoTokenForm()
        context['crypto_tokens']=crypto_tokens
        context['crypto_tokens_s']=json.dumps(CryptoTokenSerializer(crypto_tokens,many=True).data)
        return render(request,TEMPLATE_ROOT+"index.html",context)

class CryptoTokenViews(View):
    def crypto_token(self,request,*args, **kwargs):
        context=getContext(request=request)
        crypto_token=CryptoTokenRepo(request=request).crypto_token(*args, **kwargs)
        context.update(PageContext(request=request,page=crypto_token))
        context['chef_title']="CHEFFFFF TITLE"
        context['crypto_token']=crypto_token
        return render(request,TEMPLATE_ROOT+"crypto_token.html",context)
    def crypto_tokens(self,request,*args, **kwargs):
        context=getContext(request=request)
        crypto_tokens=CryptoTokenRepo(request=request).list(*args, **kwargs)
        context['crypto_tokens']=crypto_tokens
        context['crypto_tokens_s']=json.dumps(CryptoTokenSerializer(crypto_tokens,many=True).data)
        if request.user.has_perm(APP_NAME+".add_crypto_token"):
            context['add_crypto_token_form']=AddCryptoTokenForm()
        return render(request,TEMPLATE_ROOT+"crypto-tokens.html",context)