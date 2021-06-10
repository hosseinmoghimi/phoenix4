from .repo import CategoryRepo,ProductRepo
from .apps import APP_NAME

from django.shortcuts import render
TEMPLATE_ROOT=APP_NAME+"/"
from django.views import View
from core.views import CoreContext, PageContext
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['title']="Market"
    return context
# Create your views here.
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['categories']=CategoryRepo(request=request).list(for_home=True)
        context['products']=ProductRepo(request=request).list(for_home=True)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class ProductViews():
    def product(self,request,*args, **kwargs):
        
        product = ProductRepo(request).product(*args, **kwargs)
        page = product
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['product'] = product
        return render(request, TEMPLATE_ROOT+"product.html", context)
class CategoryViews():
    def category(self,request,*args, **kwargs):        
        category = CategoryRepo(request).category(*args, **kwargs)
        page = category
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['category'] = category
        context['categories'] = category.childs()
        context['products'] = category.products.all()
        return render(request, TEMPLATE_ROOT+"category.html", context)
