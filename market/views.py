from core.models import Parameter
from core.repo import ParameterRepo, PictureRepo
from core.views import CoreContext, PageContext
from django.views import View
from market.forms import AddProductForm
from .repo import CategoryRepo, ProductRepo
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
    context['layout_parent'] = LAYOUT_PARENT
    return context
# Create your views here.


class BasicViews(View):
    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['body_class']="ecommerce-page"
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['shop_header_title']=parameter_repo.parameter(name="shop_header_title")
        context['shop_header_slogan']=parameter_repo.parameter(name="shop_header_slogan")
        context['shop_header_image']=PictureRepo(request=request,app_name=APP_NAME).picture(name="shop_header_image")
        context['categories'] = CategoryRepo(
            request=request).list(for_home=True)
        context['products'] = ProductRepo(request=request).list(for_home=True)
        return render(request, TEMPLATE_ROOT+"index.html", context)


class ProductViews():
    def product(self, request, *args, **kwargs):

        product = ProductRepo(request).product(*args, **kwargs)
        page = product
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['product'] = product
        if request.user.has_perm(APP_NAME+".add_product"):
            context['add_product_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"product.html", context)


class CategoryViews():
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
