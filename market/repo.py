from utility.persian2 import PersianCalendar
from django.utils import timezone
from core import repo as CoreRepo
from messenger.repo import NotificationRepo
from market.enums import OrderLineStatusEnum, OrderStatusEnum, ShopLevelEnum
from django.http import request
from market.apps import APP_NAME
from authentication.repo import ProfileRepo
from .models import Blog, Brand, Cart, CartLine, Customer, Employee, Guarantee, Offer, Order, OrderInWareHouse, OrderLine, Product, Category, ProductFeature, ProductSpecification, Shipper, Shop, Supplier, UnitName, WareHouse
from django.db.models import Q, F
import json
class ShipperRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Shipper.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me = Shipper.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def shipper(self, *args, **kwargs):
        pk = 0
        if 'shipper_id' in kwargs:
            pk = kwargs['shipper_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()



class ProductRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Product.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def product(self, *args, **kwargs):
        if 'product_id' in kwargs:
            pk = kwargs['product_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_feature(self,*args, **kwargs):
        feature=ProductFeatureRepo(request=self.request).product_feature(*args, **kwargs)
        product=ProductRepo(request=self.request).product(*args, **kwargs)
        print(product)
        print(feature)
        print(20*"##$%")
        if product is None or feature is None:
            return None
        product.features.add(feature)
        return feature
    def add_product_for_shop(self, *args, **kwargs):
        products=[]
        # print(kwargs['specifications'])
        # print(100*"@#$")
        title = kwargs['title'] if 'title' in kwargs else None
        specifications = kwargs['specifications'] if 'specifications' in kwargs else None
        if specifications is None:
            specifications=[{'name':'size','value':'25'}]
        unit_name = kwargs['unit_name'] if 'unit_name' in kwargs else "عدد"
        if unit_name=="":
            unit_name="عدد"
        category_id = kwargs['category_id'] if 'category_id' in kwargs else None
        
        # print(specifications)
        # print(100*"@#$")
        if self.user.has_perm(APP_NAME+".add_product"):
            for specification in specifications:
                product = Product()
                product.title = title

                unit_name_ = UnitName.objects.filter(name=unit_name).first()
                if unit_name_ is None:
                    unit_name_ = UnitName()
                    unit_name_.name = unit_name
                    unit_name_.save()
                product.for_category=False
                product.save()
                product.unit_names.add(unit_name_)
                category = Category.objects.filter(pk=category_id).first()
                if category is not None:
                    category.products.add(product)
                self.add_specification(product_id=product.id,name=specification['name'],value=specification['value'])
                products.append(product)
            return products
    def add_product(self, *args, **kwargs):
        # print(kwargs['specifications'])
        # print(100*"@#$")
        title = kwargs['title'] if 'title' in kwargs else None
        specifications = kwargs['specifications'] if 'specifications' in kwargs else None
        
        unit_name = kwargs['unit_name'] if 'unit_name' in kwargs else "عدد"
        if unit_name=="":
            unit_name="عدد"
        category_id = kwargs['category_id'] if 'category_id' in kwargs else None
        
        # print(specifications)
        # print(100*"@#$")
        if self.user.has_perm(APP_NAME+".add_product"):
            product = Product()
            product.title = title

            unit_name_ = UnitName.objects.filter(name=unit_name).first()
            if unit_name_ is None:
                unit_name_ = UnitName()
                unit_name_.name = unit_name
                unit_name_.save()
            product.for_category=False
            product.save()
            product.unit_names.add(unit_name_)
            category = Category.objects.filter(pk=category_id).first()
            if category is not None:
                category.products.add(product)
            if specifications is not None:
                for specification in specifications:
                    self.add_specification(product_id=product.id,name=specification['name'],value=specification['value'])
            return product

    def add_specification(self, *args, **kwargs):

        name = kwargs['name'] if 'name' in kwargs else None
        value = kwargs['value'] if 'value' in kwargs else None
        # product_id = kwargs['product_id'] if 'product_id' in kwargs else 0
        product=self.product(*args, **kwargs)
        if product is not None:
            # ProductSpecification.objects.filter(product=product).filter(name=name).delete()
            p=ProductSpecification(product=product,name=name,value=value)
            p.save()
            return p


        


class OfferRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Offer.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def offer(self, *args, **kwargs):
        pk = 0
        if 'offer_id' in kwargs:
            pk = kwargs['offer_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class BlogRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Blog.objects
        self.me = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def blog(self, *args, **kwargs):
        pk = 0
        if 'blog_id' in kwargs:
            pk = kwargs['blog_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class SupplierRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Supplier.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me = Supplier.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def supplier(self, *args, **kwargs):
        pk = 0
        if 'supplier_id' in kwargs:
            pk = kwargs['supplier_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()


class CustomerRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Customer.objects
        self.profile = ProfileRepo(user=self.user).me
        self.me = Customer.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def customer(self, *args, **kwargs):
        pk = 0
        if 'customer_id' in kwargs:
            pk = kwargs['customer_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

class ProductFeatureRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = ProductFeature.objects
        self.profile = ProfileRepo(user=self.user).me

    def product_feature(self,*args, **kwargs):
        pk=0
        if 'product_feature_id' in kwargs:
            pk = kwargs['product_feature_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        product_feature= self.objects.filter(pk=pk).first() 

        return product_feature


class OrderRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Order.objects
        self.profile = ProfileRepo(user=self.user).me



    def orders(self,*args, **kwargs):
        return self.list(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'customer_id' in kwargs and not kwargs['customer_id']==0:
            objects = objects.filter(customer_id=kwargs['customer_id'])
        if 'customer' in kwargs:
            objects = objects.filter(customer=kwargs['customer'])
        if 'supplier_id' in kwargs and not kwargs['supplier_id']==0:
            objects = objects.filter(supplier_id=kwargs['supplier_id'])
        if 'supplier' in kwargs:
            objects = objects.filter(supplier=kwargs['supplier'])
        if 'shipper_id' in kwargs and not kwargs['shipper_id']==0:
            objects = objects.filter(shipper_id=kwargs['shipper_id'])
        if 'shipper' in kwargs:
            objects = objects.filter(shipper=kwargs['shipper'])
        
        return objects

    def order(self, *args, **kwargs):
        pk=0
        if 'order_id' in kwargs:
            pk = kwargs['order_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        order= self.objects.filter(pk=pk).first() 
        if order is not None and order.supplier.profile == self.profile:
            if order.status == OrderStatusEnum.CONFIRMED:
                order.date_accepted = timezone.now()
                order.status = OrderStatusEnum.ACCEPTED
                order.save()
        return order

    def do_pack(self, *args, **kwargs):
        order=self.order(*args, **kwargs)
        description=kwargs['description'] if 'description' in kwargs else None
        count_of_packs=kwargs['count_of_packs'] if 'count_of_packs' in kwargs else 1
        profile = self.profile
        if profile is None:
            return None
        if order.supplier.profile == profile and (order.status == OrderStatusEnum.PACKING or order.status==OrderStatusEnum.ACCEPTED):

            order.count_of_packs = count_of_packs
            if order.description is None:
                order.description = ''
            if description is not None and not description=="":
                order.description+='<br>   & ' + \
                    order.supplier.title+' : '+str(description)
            order.date_packed = timezone.now()
            order.status = OrderStatusEnum.PACKED
            order.save()
            if not order.no_ship :
                if order.customer.profile is not None:
                    NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} بسته بندی شده است.',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id}  توسط {order.supplier.title} در {order.count_of_packs} بسته آماده ارسال می باشد.',icon='alarm',profile_id=order.customer.profile.pk,color='success',priority=1)
                    
            if order is not None:
                return order

    def do_cancel(self, order_id, description):
        profile = self.profile
        if profile is None:
            return None
        order = Order.objects.get(pk=order_id)
        if order.customer.profile == profile and order.status == OrderStatusEnum.CONFIRMED:
            order.status = OrderStatusEnum.CANCELED
            if order.description is None:
                order.description = ''
            order.date_cancelled = timezone.now()
            if description is not None:
                order.description = order.description+'   @ ' + \
                    order.customer.profile.name()+' # انصراف '+PersianCalendar().from_gregorian(order.date_cancelled)+' : '+str(description)
            order.save()
            if order is not None:
                return order
    
    def confirm_order(self, order_id, description):
        profile = ProfileRepo(user=self.user).me
        if profile is None:
            return None
        order = Order.objects.get(pk=order_id)
        if order.profile == profile and order.status == OrderStatusEnum.CANCELED:
            order.status = OrderStatusEnum.CONFIRMED
            if order.description is None:
                order.description = ''
            if description is not None:
                order.description = order.description+'   @ ' + \
                    order.profile.full_name()+' # تایید مجدد '+PersianCalendar().from_gregorian(timezone.now())+' : '+str(description)
            order.save()
            if order is not None:
                return order
    
    def do_ship(self, order_id, description=''):
        shipper = ShipperRepo(user=self.user).me
        
        if shipper is None:
            return None
        order = self.order(order_id=order_id)
        if order.status == OrderStatusEnum.PACKED:
            if description is not None and not description=="":
                order.description += '<br>   & ' + \
                    shipper.title+' : '+description
            order.date_shipped = timezone.now()
            order.status = OrderStatusEnum.SHIPPED
            order.shipper = shipper
            order.save()
            if order is not None:
                if order.customer.profile is not None:
                    NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} ارسال شده است.',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id}  توسط {order.shipper.title} ارسال شده است.',icon='alarm',profile_id=order.customer.profile.pk,color='success',priority=1)
                if order.supplier.profile is not None:
                    NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} ارسال شده است.',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id}  توسط {order.shipper.title} ارسال شده است.',icon='alarm',profile_id=order.supplier.profile.pk,color='success',priority=1)
                 
                return order
        

    def do_deliver(self,*args, **kwargs):
        order=self.order(*args, **kwargs)
        description=kwargs['description'] if 'description' in kwargs else None
        ware_house_repo=WareHouseRepo(request=self.request)
        ware_house=ware_house_repo.ware_house(*args, **kwargs)

        customer = CustomerRepo(user=self.user).me
        if customer is None:
            return None 
        if order.description is None:
            order.description=""
        if order.status == OrderStatusEnum.SHIPPED or (order.status == OrderStatusEnum.PACKED and order.no_ship==True):
            if description is not None and not description=="":
                order.description +='<br>   & '+customer.profile.name+' : '+description
            order.date_delivered = timezone.now()
            order.status = OrderStatusEnum.DELIVERED
            order.save()
            if order is not None:
                if order.supplier.profile is not None:
                    NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} تحویل گرفته شد .',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id} تحویل گرفته شد.',icon='alarm',profile_id=order.supplier.profile.pk,color='success',priority=1)
                if order.customer.profile is not None:
                    NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} تحویل گرفته شد .',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id} تحویل گرفته شد.',icon='alarm',profile_id=order.customer.profile.pk,color='success',priority=1)
                if ware_house is not None:
                    ware_house_repo.add_order_in_ware_house(order=order, ware_house=ware_house, direction=True, description=description)

                return order


class GuaranteeRepo():
    def __init__(self,user=None):
        self.user=user
        self.objects=Guarantee.objects
        self.profile=ProfileRepo(user=user).me
        
    def guarantee(self,*args, **kwargs):
        pk = 0
        if 'guarantee_id' in kwargs:
            pk = kwargs['guarantee_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()



class EmployeeRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Employee.objects
        self.profile = ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        return self.objects.all()
        
    def employee(self,*args, **kwargs):
        objects = self.objects.all()
        pk=0
        if 'employee_id' in kwargs:
            pk = kwargs['employee_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        employee=objects.filter(pk=pk).first()
        return employee


class WareHouseRepo:
    def ware_house(self,*args, **kwargs):
        pk=0
        if 'ware_house_id' in kwargs:
            pk = kwargs['ware_house_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        ware_house= self.objects.filter(pk=pk).first() 
        
        return ware_house


    
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = WareHouse.objects
        self.profile = ProfileRepo(user=self.user).me

    def product_in_stock(self,pk):
        try:
            return ProductInStock.objects.get(pk=pk)
        except:
            pass
    def list(self):
        objects= self.objects.all()
        return objects
    def add_order_in_ware_house(self,*args, **kwargs):
        order_id=kwargs['order_id'] if 'order_id' in kwargs else None
        order=kwargs['order'] if 'order' in kwargs else None
        ware_house_id=kwargs['ware_house_id'] if 'ware_house_id' in kwargs else None
        ware_house=kwargs['ware_house'] if 'ware_house' in kwargs else None
        direction=kwargs['direction'] if 'direction' in kwargs else None
        description=kwargs['description'] if 'description' in kwargs else None
        if order is None:
            order=OrderRepo(request=self.request).order(pk=order_id)
        if ware_house is None:
            ware_house=self.ware_house(pk=ware_house_id)
        if order is None or ware_house is None:
            return None
        employee=Employee.objects.filter(profile=self.profile).first()
        if order is not None and ware_house is not None and employee is not None:
            order_in_warehouse=OrderInWareHouse(direction=direction,description=description,adder=employee,order=order,ware_house=ware_house)
            order_in_warehouse.save()
            return order_in_warehouse

    def add_ware_house(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_warehouse"):
            return
        name=None
        address=""
        if 'name' in kwargs:
            name=kwargs['name']
        if 'address' in kwargs:
            address=kwargs['address']
        if name is None:
            return
        ware_house=WareHouse(name=name,address=address)
        ware_house.save()
        return ware_house
        

class BrandRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Brand.objects
        self.profile = ProfileRepo(user=self.user).me

    def brand(self, *args, **kwargs):
        if 'brand_id' in kwargs:
            pk = kwargs['brand_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'cart_lines' in kwargs:
            return self.objects.filter(id__in=kwargs['cart_lines'].values('shop_id'))
        if 'product' in kwargs:
            objects = objects.filter(product=kwargs['product'])
        if 'product_id' in kwargs:
            objects = objects.filter(product_id=kwargs['product_id'])
        if 'supplier' in kwargs:
            objects = objects.filter(supplier=kwargs['supplier'])
        if 'supplier_id' in kwargs:
            objects = objects.filter(supplier_id=kwargs['supplier_id'])
        if 'region' in kwargs:
            # objects = objects.filter(supplier__in=Supplier.objects.filter(region=kwargs['region']))
            objects = objects.filter(supplier__region=kwargs['region'])
        if 'level' in kwargs:
            # objects = objects.filter(supplier__in=Supplier.objects.filter(region=kwargs['region']))
            objects = objects.filter(level=kwargs['level'])
        return objects



class ShopRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Shop.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'cart_lines' in kwargs:
            return self.objects.filter(id__in=kwargs['cart_lines'].values('shop_id'))
        if 'product' in kwargs:
            objects = objects.filter(product=kwargs['product'])
        if 'product_id' in kwargs:
            objects = objects.filter(product_id=kwargs['product_id'])
        if 'supplier' in kwargs:
            objects = objects.filter(supplier=kwargs['supplier'])
        if 'supplier_id' in kwargs:
            objects = objects.filter(supplier_id=kwargs['supplier_id'])
        if 'level' in kwargs:
            objects = objects.filter(level=kwargs['level'])
        if 'region' in kwargs:
            # objects = objects.filter(supplier__in=Supplier.objects.filter(region=kwargs['region']))
            objects = objects.filter(supplier__region=kwargs['region'])
        return objects
    def confirm_cart(self,*args, **kwargs):
        quantity=0
        shop=None
        if 'shop' in kwargs:
            shop=kwargs['shop']
            shop=self.shop(pk=shop.id)
        if 'quantity' in kwargs:
            quantity=kwargs['quantity']
        if shop is not None:
            shop.available=shop.available-quantity
            shop.save()

    def add_shop(self, *args, **kwargs):
        product_id = 0
        supplier_id = 0
        unit_name = ""
        unit_price = 0
        available = 100
        specifications=[]
        level=ShopLevelEnum.REGULAR
        if 'specifications' in kwargs:
            specifications = kwargs['specifications']
        if 'level' in kwargs:
            level = kwargs['level']
        if 'product_id' in kwargs:
            product_id = kwargs['product_id']
        if 'supplier_id' in kwargs:
            supplier_id = kwargs['supplier_id']
        if 'unit_name' in kwargs:
            unit_name = kwargs['unit_name']
        if 'unit_price' in kwargs:
            unit_price = kwargs['unit_price']
        if 'available' in kwargs:
            available = kwargs['available']
        if not available>0 or unit_price==0:
            Shop.objects.filter(supplier_id=supplier_id).filter(level=level).filter(product_id=product_id).filter(unit_name=unit_name).delete()
            return {'result':'deleted'}
        shop = Shop.objects.filter(supplier_id=supplier_id).filter(level=level).filter(product_id=product_id).filter(unit_name=unit_name).first()
        if shop is None:
            shop = Shop(
                supplier_id=supplier_id,
                product_id=product_id,
                level=level,
                unit_name=unit_name,
                unit_price=unit_price,
                available=available
            )
            shop.save()
            
            if len(specifications)>0:
                for specification in specifications:
                    specification=ProductSpecification.objects.filter(pk=specification['id']).first()
                    shop.specifications.add(specification)
            return shop
        else:
            # shops=Shop.objects.filter(supplier_id=supplier_id).filter(level=level).filter(product_id=product_id).filter(unit_name=unit_name).exclude(pk=shop.id)
            # shops.delete()
            
            # shop.available = available
            # shop.unit_price = unit_price
            # shop.level = level
            shop = Shop(
                supplier_id=supplier_id,
                product_id=product_id,
                level=level,
                unit_name=unit_name,
                unit_price=unit_price,
                available=available
            )
            shop.save()
            
            if len(specifications)>0:
                for specification in specifications:
                    specification=ProductSpecification.objects.filter(pk=specification['id']).first()
                    shop.specifications.add(specification)

            return shop
    def shop(self,*args, **kwargs):
        objects = self.objects.all()
        pk=0
        if 'shop_id' in kwargs:
            pk = kwargs['shop_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        shop=objects.filter(pk=pk).first()
        return shop
class CartLineRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = CartLine.objects
        self.profile = ProfileRepo(user=self.user).me


class CartRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Cart.objects
        self.profile = ProfileRepo(user=self.user).me

    def cart(self, *args, **kwargs):
        objects = self.objects.all()
        customer_id=0
        if 'customer' in kwargs:
            customer = kwargs['customer']
            customer_id=customer.id
        elif 'customer_id' in kwargs:
            customer_id = kwargs['customer_id']
            customer=Customer.objects.filter(pk=customer_id).first()
        cart=objects.filter(customer_id=customer_id).first()
        if cart is None:
            cart=Cart()
            cart.customer=customer
            cart.save()

        cart.lines=CartLine.objects.filter(customer=customer)
        cart.orders=self.get_cart_orders(customer_id=customer_id)
        return cart
    
    def get_cart_orders(self,customer_id=0,no_ship=None):
        if no_ship is None:
            no_ship=False
        if customer_id ==0:
            customer=CustomerRepo(user=self.user).me
        else:
            customer=CustomerRepo(user=self.user).customer(customer_id=customer_id)
        cart_lines = CartLine.objects.filter(customer=customer)
        if len(cart_lines)==0:
            return None
        shops =ShopRepo(user=self.user).list(cart_lines=cart_lines)
        orders=[]
        for supplier in Supplier.objects.filter(id__in=shops.values('supplier_id')):
            order = Order()
            order.status=OrderStatusEnum.CART
            order.supplier = supplier
            order.customer_id = customer_id
            if no_ship:
                order.ship_fee = 0
            else:
                order.ship_fee = supplier.ship_fee
            order.status = OrderStatusEnum.CONFIRMED
            order.description = ''
            order.address = ''
            order.no_ship = no_ship
            # order.total=order.ship_fee
            # order.save()
            order.lines=[]
            if order is not None:
                for cart_line in cart_lines:
                    if cart_line.shop.supplier == supplier:
                        order_line=OrderLine(order=order, product=cart_line.shop.product, quantity=cart_line.quantity,
                                    unit_price=cart_line.shop.unit_price, unit_name=cart_line.shop.unit_name,status=OrderLineStatusEnum.CART)
                        # order_line.save()
                        order.lines.append(order_line)
                        # order.total+=cart_line.shop.unit_price*cart_line.quantity
                
                orders.append(order)
        
        return orders
    
    
    def checkout(self,*args, **kwargs):
        cart_lines=kwargs['cart_lines'] if 'cart_lines' in kwargs else None
        customer_id=kwargs['customer_id'] if 'customer_id' in kwargs else None
        if cart_lines is None or customer_id is None:
            return None
        user=self.user
        if customer_id is None:
            customer=CustomerRepo(user=self.user).me
        else:
            customer = CustomerRepo(user=self.user).customer(customer_id=customer_id)
        if customer is not None:
            # delete old cart_lines
            CartLine.objects.filter(customer=customer).delete()
            
            # create new cart_lines
            for cart_line in cart_lines:
                if cart_line['quantity']>0:
                    new_cart_line=CartLine(shop=Shop.objects.get(pk=cart_line['shop_id']),quantity=cart_line['quantity'],customer=customer)
                    new_cart_line.save()
            # get new cart_lines
            cart_lines = CartLine.objects.filter(customer=customer)
            return cart_lines
                 
    def add_to_cart(self,*args, **kwargs):
        customer=CustomerRepo(request=self.request).me
        if customer is not None:
            shop_id=kwargs['shop_id']
            quantity=kwargs['quantity']
            shop=ShopRepo(request=self.request).shop(*args, **kwargs)
            if shop is None:
                return
            if shop.available<quantity:
                return
            lines=CartLine.objects.filter(customer=customer).filter(shop_id=shop_id)
            lines.delete()
            if quantity>0 :
                cart_line=CartLine(shop_id=shop_id,quantity=quantity,customer=customer)
                cart_line.save()
                cart=Cart.objects.filter(customer=customer).first()
                return cart_line

    def confirm(self,*args, **kwargs):
        
        no_ship=kwargs['no_ship'] if 'no_ship' in kwargs else False
        customer_id=kwargs['customer_id'] if 'customer_id' in kwargs else None
        description=kwargs['description'] if 'description' in kwargs else None
        supplier_id=kwargs['supplier_id'] if 'supplier_id' in kwargs else None
        address=kwargs['address'] if 'address' in kwargs else None
        user=self.user
        if customer_id is None:
            customer=CustomerRepo(user=self.user).me
        else:
            customer = CustomerRepo(user=self.user).customer(customer_id=customer_id)
            
        if customer is not None:
            cart_lines = CartLine.objects.filter(customer=customer)
            shops = ShopRepo(user=self.user).list(cart_lines=cart_lines)
            orders=[]
            if supplier_id==0:
                suppliers=Supplier.objects.filter(id__in=shops.values('supplier_id'))
            else:
                suppliers=[SupplierRepo(user=self.user).supplier(supplier_id=supplier_id)]
            for supplier in suppliers:
                order = Order()
                order.supplier_id = supplier.id
                order.customer = customer
                if no_ship:
                    order.ship_fee = 0
                else:
                    order.ship_fee = supplier.ship_fee
                order.status = OrderStatusEnum.CONFIRMED
                order.description = description
                order.address = address
                order.no_ship = no_ship
                from django.utils import timezone
                order.date_ordered =  timezone.now()
                order.save()
                if order is not None:
                    orders.append(order)
                    for cart_line in cart_lines:
                        if cart_line.shop.supplier == supplier:
                            order_line=OrderLine(
                                order=order,
                                product=cart_line.shop.product,
                                quantity=cart_line.quantity,
                                unit_price=cart_line.shop.unit_price,
                                #product_title=cart_line.shop.product.title,
                                unit_name=cart_line.shop.unit_name)
                            order_line.save()
                            ShopRepo(request=self.request).confirm_cart(shop=cart_line.shop,quantity=cart_line.quantity)
                            cart_line.delete()
                    # order=OrderRepo(user=self.user).get(order_id=order.pk)
                    # MyPusherChannel(user=self.user).submit(order_id=order.id,total=order.total(),supplier_id=order.supplier.id)
                    if order.supplier.profile is not None:
                        NotificationRepo(request=self.request).add(
                            title='سفارش تایید شده',
                            body=f'سفارش تایید شده به مبلغ {order.total} تومان',
                            url=order.get_absolute_url(),
                            icon='alarm',
                            profile_id=order.supplier.profile.pk,
                            color='danger',priority=1
                            )
                    # ProfileTransactionRepo(user=self.user).add(
                    #     profile_bestankar=order.supplier.profile,
                    #     profile_bedehkar=order.customer.profile,amount=order.total(),description=f'فاکتور شماره {order.id}')
                    
            
            return orders

class CategoryRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Category.objects
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=True) | Q(parent=None))
        return objects

    def category(self, *args, **kwargs):
        if 'category_id' in kwargs:
            pk = kwargs['category_id']
        elif 'pk' in kwargs:
            pk = kwargs['pk']
        elif 'id' in kwargs:
            pk = kwargs['id']
        return self.objects.filter(pk=pk).first()

    def add_category(self, *args, **kwargs):
        title = kwargs['title'] if 'title' in kwargs else None
        parent_id = kwargs['parent_id'] if 'parent_id' in kwargs else None
        if title is None or parent_id is None:
            return None
        if self.user.has_perm(APP_NAME+".add_category"):
            category = Category()
            category.title = title
            if parent_id > 0:
                category.parent_id = parent_id
            category.save()
            return category
