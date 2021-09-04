from market.apps import APP_NAME
from authentication.repo import ProfileRepo
from .models import Product,Category, UnitName
from django.db.models import Q,F
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
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'category_id' in kwargs:
            return CategoryRepo(self.request).category(category_id=kwargs['category_id']).products.all()
        return objects
    def product(self,*args, **kwargs):
        if 'product_id' in kwargs:
            pk=kwargs['product_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_product(self,*args, **kwargs):
        
        title=kwargs['title'] if 'title' in kwargs else None
        unit_name=kwargs['unit_name'] if 'unit_name' in kwargs else "عدد"
        category_id=kwargs['category_id'] if 'category_id' in kwargs else None
        if self.user.has_perm(APP_NAME+".add_product"):
            product=Product()
            product.title=title

            unit_name_=UnitName.objects.filter(name=unit_name).first()
            print(unit_name_)
            print(10*"#5456")
            if unit_name_ is None:
                unit_name_=UnitName()
                unit_name_.name=unit_name
                unit_name_.save()
                print(unit_name_)
                print(10*"#2323")
            product.save()
            product.unit_names.add(unit_name_)
            category=Category.objects.filter(pk=category_id).first()
            if category is not None:
                category.products.add(product)
            return product
    



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
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(Q(for_home=True)|Q(parent=None))
        return objects
    def category(self,*args, **kwargs):
        if 'category_id' in kwargs:
            pk=kwargs['category_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_category(self,*args, **kwargs):
        title=kwargs['title'] if 'title' in kwargs else None
        parent_id=kwargs['parent_id'] if 'parent_id' in kwargs else None
        if title is None or parent_id is None:
            return None
        if self.user.has_perm(APP_NAME+".add_category"):
            category=Category()
            category.title=title
            if parent_id>0:
                category.parent_id=parent_id
            category.save()
            return category
    