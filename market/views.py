from core.serializers import ImageSerializer
import json
from market.enums import ParameterEnum
from core.models import Parameter
from core.repo import ParameterRepo, PictureRepo
from core.views import CoreContext, PageContext
from django.views import View
from market.forms import AddProductForm
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
        context['categories'] = CategoryRepo(request=request).list(for_home=True)
        context['offers'] = OfferRepo(request=request).list(for_home=True)
        context['blogs'] = BlogRepo(request=request).list(for_home=True)
        context['products'] = ProductRepo(request=request).list(for_home=True)
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
        context['me_supplier']=SupplierRepo(request=request).me
        me_customer=CustomerRepo(request=request).me
        print(me_customer)
        context['me_customer']=CustomerRepo(request=request).me
        # context['images_s']=json.dumps(ImageSerializer(product.images(),many=True).data)
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
        context['categories'] = category.childs()
        context['products'] = category.products.all()
        if request.user.has_perm(APP_NAME+".add_product"):
            context['add_product_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"category.html", context)
