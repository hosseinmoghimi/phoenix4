from market.serializers import ShopSerializer
from core.serializers import ImageSerializer
import json
from market.enums import ParameterEnum, ShopLevelEnum
from core.models import Parameter
from core.repo import ParameterRepo, PictureRepo
from core.views import CoreContext, PageContext
from django.views import View
from market.forms import AddCategoryForm, AddProductForm
from .repo import BlogRepo, CategoryRepo, CustomerRepo, OfferRepo, ProductRepo, SupplierRepo
from .apps import APP_NAME

from django.shortcuts import render
TEMPLATE_ROOT = "market/"
LAYOUT_PARENT = "Adminlte/layout.html"
LAYOUT_PARENT="Adminlte/layout.html"
LAYOUT_PARENT="phoenix/layout.html"
LAYOUT_PARENT="material-kit-pro/layout.html"

def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['title'] = "Market"
    
    context['me_supplier']=SupplierRepo(request=request).me
    context['me_customer']=CustomerRepo(request=request).me
    context['navbar']=APP_NAME+"/includes/nav-bar.html"
    context['layout_parent'] = LAYOUT_PARENT
    context['root_categories'] = CategoryRepo(
            request=request).list(for_home=True)
    return context
# Create your views here.


class BasicViews(View):
    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['body_class']="ecommerce-page"
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['shop_header_title']=parameter_repo.parameter(name=ParameterEnum.SHOP_HEADER_TITLE)
        context['shop_header_slogan']=parameter_repo.parameter(name=ParameterEnum.SHOP_HEADER_SLOGAN)
        context['shop_header_image']=PictureRepo(request=request,app_name=APP_NAME).picture(name=ParameterEnum.SHOP_HEADER_IMAGE)
        categories= CategoryRepo(request=request).list(for_home=True)
        context['categories'] = categories
        context['offers'] = OfferRepo(request=request).list(for_home=True)
        context['blogs'] = BlogRepo(request=request).list(for_home=True)
        products = ProductRepo(request=request).list(for_home=True)
        context['products'] = products
        context['top_products'] = products.order_by('-priority')[:3]
        if request.user.has_perm(APP_NAME+".add_product") and len(categories)==0:
            context['add_product_form'] = AddProductForm()
        if request.user.has_perm(APP_NAME+".add_category") and len(products)==0:
            context['add_category_form'] = AddCategoryForm()
        return render(request, TEMPLATE_ROOT+"index.html", context)

class CartViews(View):
    def cart(self, request, *args, **kwargs):

        product = ProductRepo(request).product(*args, **kwargs)
        page = product
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['product'] = product
        context['body_class']="product-page"
        if request.user.has_perm(APP_NAME+".add_product"):
            context['add_product_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"product.html", context)

class ProductViews(View):
    def product(self, request, *args, **kwargs):

        product = ProductRepo(request).product(*args, **kwargs)
        page = product
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['product'] = product
        context['shop_levels']=(i[0] for i in ShopLevelEnum.choices)
        if context['me_customer'] is not None:
            context['shops_s']=json.dumps(ShopSerializer(product.shop_set.filter(level=context['me_customer'].level),many=True).data)
        context['body_class']="product-page"
        return render(request, TEMPLATE_ROOT+"product.html", context)


class SupplierViews(View):
    def supplier(self, request, *args, **kwargs):

        supplier = SupplierRepo(request).supplier(*args, **kwargs)
        page = supplier
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['supplier'] = supplier
        context['body_class']="product-page"
        return render(request, TEMPLATE_ROOT+"supplier.html", context)


class OfferViews(View):
    def offer(self, request, *args, **kwargs):

        offer = OfferRepo(request).offer(*args, **kwargs)
        page = offer
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['offer'] = offer
        if request.user.has_perm(APP_NAME+".add_offer"):
            context['add_offer_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"offer.html", context)


class BlogViews(View):
    def blog(self, request, *args, **kwargs):

        blog = BlogRepo(request).blog(*args, **kwargs)
        page = blog
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['blog'] = blog
        if request.user.has_perm(APP_NAME+".add_blog"):
            context['add_blog_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"blog.html", context)

class CategoryViews(View):
    def category(self, request, *args, **kwargs):
        category = CategoryRepo(request).category(*args, **kwargs)
        page = category
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['category'] = category
        categories= category.childs()
        context['categories'] =categories
        products= category.products.all()
        context['products'] = products
        context['top_products'] = products.filter(for_category=True)[:3]
        if request.user.has_perm(APP_NAME+".add_product") and len(categories)==0:
            context['add_product_form'] = AddProductForm()
        if request.user.has_perm(APP_NAME+".add_category") and len(products)==0:
            context['add_category_form'] = AddCategoryForm()
        return render(request, TEMPLATE_ROOT+"category.html", context)
