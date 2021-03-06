import json

from django.db.models import manager
from market.forms import *
from market.serializers import CartLineSerializer, CategorySerializer, GuaranteeSerializer, OrderSerializer, ProductFeatureSerializer, ProductSerializer, ProductSpecificationSerializer, ShopSerializer, UnitNameSerializer, WareHouseSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from core.constants import SUCCEED,FAILED
from utility.persian import PersianCalendar
from .repo import CartRepo, CategoryRepo, GuaranteeRepo, OrderRepo, ProductRepo, ShopRepo, WareHouseRepo
from .apps import APP_NAME

 
class GuaranteeApi(APIView):
    def add_guarantee(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_guarantee_form=AddGuaranteeForm(request.POST)
            if add_guarantee_form.is_valid():
                log=3
                order_line_id=add_guarantee_form.cleaned_data['order_line_id']
                barcode=add_guarantee_form.cleaned_data['barcode']
                serial_no=add_guarantee_form.cleaned_data['serial_no']
                end_date=add_guarantee_form.cleaned_data['end_date']
                start_date=add_guarantee_form.cleaned_data['start_date']
                description=add_guarantee_form.cleaned_data['description']

                end_date=PersianCalendar().to_gregorian(end_date)
                start_date=PersianCalendar().to_gregorian(start_date)
 
                guarantee=GuaranteeRepo(request=request).add_guarantee(
                    order_line_id=order_line_id,
                    start_date=start_date,
                    end_date=end_date,
                    serial_no=serial_no,
                    description=description,
                    barcode=barcode)
                if guarantee is not None:
                    context['guarantee']=GuaranteeSerializer(guarantee).data
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
            
                specifications=add_shop_form.cleaned_data['specifications']
                unit_name=add_shop_form.cleaned_data['unit_name']
                unit_price=add_shop_form.cleaned_data['unit_price']
                buy_price=add_shop_form.cleaned_data['buy_price']
                level=add_shop_form.cleaned_data['level']
                old_price=add_shop_form.cleaned_data['old_price']
                available=add_shop_form.cleaned_data['available']
                product_id=add_shop_form.cleaned_data['product_id']
                supplier_id=add_shop_form.cleaned_data['supplier_id']
                shop=ShopRepo(request=request).add_shop(
                    unit_price=unit_price,
                    old_price=old_price,
                    buy_price=buy_price,
                    unit_name=unit_name,
                    level=level,
                    specifications=json.loads(specifications),
                    available=available,
                    product_id=product_id,
                    supplier_id=supplier_id,
                    )
                if shop is not None:
                    # shops=ProductRepo(request=request).product(pk=product_id).shop_set.all()
                    context['shop']=ShopSerializer(shop).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class OrderApi(APIView):
    def save_order(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            save_order_form=SaveOrderForm(request.POST)
            if save_order_form.is_valid():
                log=3
                cd=save_order_form.cleaned_data
                supplier_id=cd['supplier_id']
                customer_id=cd['customer_id']
                description=cd['description']
                order_lines=cd['order_lines']
                order=OrderRepo(request=request).add_order(
                    supplier_id=supplier_id,
                    customer_id=customer_id,
                    order_lines=order_lines,
                    description=description,
                    )
                if order is not None:
                    context['order']=OrderSerializer(order).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def edit_order_line(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            edit_order_line_form=EditOrderLineForm(request.POST)
            if edit_order_line_form.is_valid():
                log=3
                order_id=edit_order_line_form.cleaned_data['order_id']
                product_id=edit_order_line_form.cleaned_data['product_id']
                unit_name=edit_order_line_form.cleaned_data['unit_name']
                unit_price=edit_order_line_form.cleaned_data['unit_price']
                quantity=edit_order_line_form.cleaned_data['quantity']
                cart_line=CartRepo(request=request).add_to_cart(
                    product_id=product_id,
                    order_id=order_id,
                    unit_name=unit_name,
                    unit_price=unit_price,
                    quantity=quantity,
                    )
                if cart_line is not None:
                    context['cart_line']=CartLineSerializer(cart_line).data
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
    def save_cart(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            checkout_cart_form=CheckoutCartForm(request.POST)
            if checkout_cart_form.is_valid():
                log=3
                cart_lines=checkout_cart_form.cleaned_data['cart_lines']
                customer_id=checkout_cart_form.cleaned_data['customer_id']
                cart_lines=json.loads(cart_lines)
                cart_lines=CartRepo(request=request).save(
                    cart_lines=cart_lines,
                    customer_id=customer_id
                    )
                if cart_lines is not None:
                    level=4
                    cart_lines_s=CartLineSerializer(cart_lines,many=True).data
                    context['cart_lines']=cart_lines_s
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
 

class WareHouseApi(APIView):
    def add_warehouse(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_warehouse_form=AddWareHouseForm(request.POST)
            if add_warehouse_form.is_valid():
                log=3
                name=add_warehouse_form.cleaned_data['name']
                address=add_warehouse_form.cleaned_data['address']
                ware_house=WareHouseRepo(request=request).add_ware_house(name=name,address=address)
                if ware_house is not None:
                    log=4
                    ware_house=WareHouseSerializer(ware_house).data
                    context['ware_house']=ware_house
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)      


class ProductApi(APIView):
    def select_product(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            select_product_form=SelectProductForm(request.POST)
            if select_product_form.is_valid():
                log=3
                cd=select_product_form.cleaned_data
                product_id=cd['product_id']
                barcode=cd['barcode']
                
                product=ProductRepo(request=request).product(barcode=barcode,product_id=product_id)
                if product is not None:
                    log=4
                    context['product']=ProductSerializer(product).data
                    unit_names=product.unit_names.all()
                    context['unit_names']=UnitNameSerializer(unit_names,many=True).data
                    unit_names
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def add_feature_for_product(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_product_feature_form=AddProductFeatureForm(request.POST)
            if add_product_feature_form.is_valid():
                log=3
                product_id=add_product_feature_form.cleaned_data['product_id']
                product_feature_id=add_product_feature_form.cleaned_data['product_feature_id']
                add_or_remove=add_product_feature_form.cleaned_data['add_or_remove']
                
                feature=ProductRepo(request=request).add_feature(add_or_remove=add_or_remove,product_id=product_id,product_feature_id=product_feature_id)
                if feature is not None:
                    log=4
                    context['feature']=ProductFeatureSerializer(feature).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
    
    def add_product_specification(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_product_specification_form=AddProductSpecificationForm(request.POST)
            if add_product_specification_form.is_valid():
                product_id=add_product_specification_form.cleaned_data['product_id']
                name=add_product_specification_form.cleaned_data['name']
                value=add_product_specification_form.cleaned_data['value']
                
                product_specification=ProductRepo(request=request).add_specification(product_id=product_id,name=name,value=value)
                if product_specification is not None:
                    context['product_specification']=ProductSpecificationSerializer(product_specification).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
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
                specifications=add_product_form.cleaned_data['specifications']
                category_id=add_product_form.cleaned_data['category_id']
                
                if specifications is None or specifications=="":
                    specifications=None
                else:
                    specifications=json.loads(specifications)
                product=ProductRepo(request=request).add_product(
                    title=title,
                    unit_name=unit_name,
                    specifications=specifications,
                    category_id=category_id)
                if product is not None:
                    context['product']=ProductSerializer(product).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
    def add_product_for_shoe(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_product_for_shoe_form=AddProductForShoeForm(request.POST)
            if add_product_for_shoe_form.is_valid():
                log=3
                category_id=add_product_for_shoe_form.cleaned_data['category_id']
                title=add_product_for_shoe_form.cleaned_data['title']
                unit_name=add_product_for_shoe_form.cleaned_data['unit_name']
                availables=add_product_for_shoe_form.cleaned_data['availables']
                unit_price=add_product_for_shoe_form.cleaned_data['unit_price']
                old_price=add_product_for_shoe_form.cleaned_data['old_price']
                buy_price=add_product_for_shoe_form.cleaned_data['buy_price']
                supplier_id=add_product_for_shoe_form.cleaned_data['supplier_id']
                barcode=add_product_for_shoe_form.cleaned_data['barcode']
                
                if availables is None or availables=="":
                    availables=None
                else:
                    availables=json.loads(availables)
                product=ProductRepo(request=request).add_product_for_shoe(
                    category_id=category_id,
                    title=title,
                    unit_name=unit_name,
                    barcode=barcode,
                    supplier_id=supplier_id,
                    unit_price=unit_price,
                    buy_price=buy_price,
                    old_price=old_price,
                    availables=availables,
                    )
                if product is not None:
                    context['product']=ProductSerializer(product).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
        
    def add_product_for_shop(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            add_product_for_shop_form=AddProductForShopForm(request.POST)
            if add_product_for_shop_form.is_valid():
                log=3
                title=add_product_for_shop_form.cleaned_data['title']
                unit_name=add_product_for_shop_form.cleaned_data['unit_name']
                specifications=add_product_for_shop_form.cleaned_data['specifications']
                category_id=add_product_for_shop_form.cleaned_data['category_id']
                supplier_id=add_product_for_shop_form.cleaned_data['supplier_id']
                
                if specifications is None or specifications=="":
                    specifications=None
                else:
                    specifications=json.loads(specifications)
                product=ProductRepo(request=request).add_product(
                    title=title,
                    unit_name=unit_name,
                    specifications=specifications,
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
   