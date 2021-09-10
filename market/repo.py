from market.enums import ShopLevelEnum
from django.http import request
from market.apps import APP_NAME
from authentication.repo import ProfileRepo
from .models import Blog, CartLine, Customer, Offer, Product, Category, Shop, Supplier, UnitName
from django.db.models import Q, F


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

    def add_product(self, *args, **kwargs):

        title = kwargs['title'] if 'title' in kwargs else None
        unit_name = kwargs['unit_name'] if 'unit_name' in kwargs else "عدد"
        if unit_name=="":
            unit_name="عدد"
        print(unit_name=="")
        print(unit_name is None)
        print(10*"#")
        category_id = kwargs['category_id'] if 'category_id' in kwargs else None
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
            return product


class CartRepo:
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
    def add_to_cart(self,*args, **kwargs):
        customer=CustomerRepo(request=self.request).me
        if customer is not None:
            shop_id=kwargs['shop_id']
            quantity=kwargs['quantity']
            lines=CartLine.objects.filter(customer=customer).filter(shop_id=shop_id)
            lines.delete()
            cart_line=CartLine(shop_id=shop_id,quantity=quantity,customer=customer)
            cart_line.save()
            return cart_line
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
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects

    def add_shop(self, *args, **kwargs):
        product_id = 0
        supplier_id = 0
        unit_name = ""
        unit_price = 0
        available = 100
        level=ShopLevelEnum.REGULAR
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
            return shop
        else:
            shops=Shop.objects.filter(supplier_id=supplier_id).filter(level=level).filter(product_id=product_id).filter(unit_name=unit_name).exclude(pk=shop.id)
            shops.delete()
            shop.available = available
            shop.unit_price = unit_price
            shop.level = level
            shop.save()
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

    def cart(self, *args, **kwargs):
        objects = self.objects.all()
        if 'customer' in kwargs:
            customer = kwargs['customer']
        elif 'customer_id' in kwargs:
            customer_id = kwargs['customer_id']
            customer=Customer.objects.filter(pk=customer_id)
        cart={}
        cart['lines']=objects.filter(customer=customer)

        return cart

    def add_shop(self, *args, **kwargs):
        product_id = 0
        supplier_id = 0
        unit_name = ""
        unit_price = 0
        available = 100
        level=ShopLevelEnum.REGULAR
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
            return shop
        else:
            shops=Shop.objects.filter(supplier_id=supplier_id).filter(level=level).filter(product_id=product_id).filter(unit_name=unit_name).exclude(pk=shop.id)
            shops.delete()
            shop.available = available
            shop.unit_price = unit_price
            shop.level = level
            shop.save()
            return shop


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
