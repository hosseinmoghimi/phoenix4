import json
from urllib.parse import urlparse

from django.db.models import manager
from market.forms import *
from market.apk_serializers import CartLineSerializer, CategorySerializer, GuaranteeSerializer, OrderSerializer, ProductFeatureSerializer, ProductSerializer, ProductSpecificationSerializer, ShopSerializer, UnitNameSerializer, WareHouseSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
from utility.persian import PersianCalendar
from .repo import CartRepo, CategoryRepo, GuaranteeRepo, OrderRepo, ProductRepo, ShopRepo, WareHouseRepo
from .apps import APP_NAME
from django.urls import path
class CategoryApi(APIView):
    def categories(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        categories=CategorySerializer(CategoryRepo(request=request).list(),many=True).data
        context['categoies']=categories
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


urlpatterns=[
    path("categories/",CategoryApi().categories,name="apk_categories"),

]