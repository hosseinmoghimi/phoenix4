from market.serializers import ProductSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
from .repo import ProductRepo
from .apps import APP_NAME
from django.urls import path,include



class ProductApi(APIView):
    def products(self,request,category_id,*args, **kwargs):
        context={}
        context['result']=SUCCEED
        products=ProductRepo(request=request).list(category_id=category_id)
        context['products']=ProductSerializer(products,many=True).data
        return JsonResponse(context)
        


app_name=APP_NAME
urlpatterns = [

    path("products/<int:category_id>/",ProductApi().products,name="products"),

    
]