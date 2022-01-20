import json
from unicodedata import category
from urllib.parse import urlparse

from django.db.models import manager
from authentication.repo import ProfileRepo
from market.forms import *
from market.apk_serializers import CartSerializer, CustomerSerializer, ProductFullSerializer,CartLineSerializer, CategorySerializer, GuaranteeSerializer, OrderSerializer, ProductFeatureSerializer, ProductSerializer, ProductSpecificationSerializer, ShopSerializer, UnitNameSerializer, WareHouseSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
from utility.persian import PersianCalendar
from .repo import CartRepo, CategoryRepo, CustomerRepo, GuaranteeRepo, OrderRepo, ProductRepo, ShopRepo, WareHouseRepo
from .apps import APP_NAME
from django.urls import path
class CategoryApi(APIView):
    def categories(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        categories=CategorySerializer(CategoryRepo(request=request).list(),many=True).data
        context['categories']=categories
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.views import ObtainAuthToken
class CartApi(ObtainAuthToken):

    authentication_classes = [TokenAuthentication]
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        token=request.headers['token']
        # context['token']=token
        request=ProfileRepo(request=request).login_by_token()
        context['username']=request.user.username
        customer=CustomerRepo(request=request).me
        cart=CartRepo(request=request).cart(customer=customer)
        # context['cart']=CartSerializer(cart).data
        context['cartLines']=CartLineSerializer(cart.lines,many=True).data
        context['result']=SUCCEED
        context['customer']=CustomerSerializer(customer).data
        context['log']=log
        return JsonResponse(context)




class ProductApi(APIView):
    def products(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        products=ProductSerializer(ProductRepo(request=request).list(*args, **kwargs),many=True).data
        context['products']=products
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def product(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        products=ProductFullSerializer(ProductRepo(request=request).product(*args, **kwargs)).data
        context['product']=products
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

urlpatterns=[
    path("categories/",CategoryApi().categories),
    path("products/<int:category_id>/",ProductApi().products),
    path("product/<int:product_id>/",ProductApi().product),
    path("cart/",CartApi.as_view()),

]