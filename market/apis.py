from market.forms import *
from market.serializers import CartLineSerializer, CategorySerializer, ProductSerializer, ShopSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
from .repo import CartRepo, CategoryRepo, ProductRepo, ShopRepo
from .apps import APP_NAME

class categoryApi(APIView):
    def add_category(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_category_form=AddCategoryForm(request.POST)
            if add_category_form.is_valid():
                log=3
                title=add_category_form.cleaned_data['title']
                parent_id=add_category_form.cleaned_data['parent_id']
                category=CategoryRepo(request=request).add_category(title=title,parent_id=parent_id)
                if category is not None:
                    context['category']=CategorySerializer(category).data
                    context['result']=SUCCEED
        return JsonResponse(context)

class ShopApi(APIView):
    def add_shop(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_shop_form=AddShopForm(request.POST)
            if add_shop_form.is_valid():
                log=3
                unit_price=add_shop_form.cleaned_data['unit_price']
                unit_name=add_shop_form.cleaned_data['unit_name']
                level=add_shop_form.cleaned_data['level']
                available=add_shop_form.cleaned_data['available']
                product_id=add_shop_form.cleaned_data['product_id']
                supplier_id=add_shop_form.cleaned_data['supplier_id']
                shop=ShopRepo(request=request).add_shop(
                    unit_price=unit_price,
                    unit_name=unit_name,
                    level=level,
                    available=available,
                    product_id=product_id,
                    supplier_id=supplier_id,
                    )
                if shop is not None:
                    shops=ProductRepo(request=request).product(pk=product_id).shop_set.all()
                    context['shops']=ShopSerializer(shops,many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
      
class CartApi(APIView):
    def add_to_cart(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_to_cart_form=AddToCartForm(request.POST)
            if add_to_cart_form.is_valid():
                log=3
                shop_id=add_to_cart_form.cleaned_data['shop_id']
                quantity=add_to_cart_form.cleaned_data['quantity']
                cart_line=CartRepo(request=request).add_to_cart(
                    shop_id=shop_id,
                    quantity=quantity,
                    )
                if cart_line is not None:
                    context['cart_line']=CartLineSerializer(cart_line).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
class CategoryApi(APIView):
    def add_category(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_category_form=AddCategoryForm(request.POST)
            if add_category_form.is_valid():
                log=3
                title=add_category_form.cleaned_data['title']
                parent_id=add_category_form.cleaned_data['parent_id']
                category=CategoryRepo(request=request).add_category(
                    title=title,
                    parent_id=parent_id)
                if category is not None:
                    context['category']=CategorySerializer(category).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
      
class ProductApi(APIView):
    def add_product(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_product_form=AddProductForm(request.POST)
            if add_product_form.is_valid():
                log=3
                title=add_product_form.cleaned_data['title']
                unit_name=add_product_form.cleaned_data['unit_name']
                category_id=add_product_form.cleaned_data['category_id']
                product=ProductRepo(request=request).add_product(
                    title=title,
                    unit_name=unit_name,
                    category_id=category_id)
                if product is not None:
                    context['product']=ProductSerializer(product).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
    def products(self,request,category_id,*args, **kwargs):
        context={}
        context['result']=SUCCEED
        products=ProductRepo(request=request).list(category_id=category_id)
        context['products']=ProductSerializer(products,many=True).data
        return JsonResponse(context)
   