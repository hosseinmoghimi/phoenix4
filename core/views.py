from core.apis import BasicApi
from django.shortcuts import render
from .apps import APP_NAME
from .forms import *
from .repo import *
from .settings import *
from .enums import *
from .utils import AdminUtility
from .constants import *
from django.views import View
TEMPLATE_ROOT="core/"
def PageContext(request,page):
    context={}
    context['page']=page
    context['parent_id']=page.id

    if request.user.has_perm(APP_NAME+".add_pagelink"):
        context['add_page_link_form']=AddPageLinkForm()
    return context
def getContext(request):
    context=DefaultContext(request=request,app_name=APP_NAME)
    context["layout_root"]=TEMPLATE_ROOT+"/layout.html"
    context["admin_utility"]=AdminUtility(request=request)
    return context
# Create your views here.
def CoreContext(request,app_name,*args, **kwargs):
    context={}
    context['user']=request.user
    context['profile']=ProfileRepo(user=request.user).me
    context['APP_NAME']=app_name
    
    context[app_name+'_sidebar']=True
    context['DEBUG']=DEBUG
    context['ADMIN_URL']=ADMIN_URL
    context['MEDIA_URL']=MEDIA_URL
    context['SITE_URL']=SITE_URL
    context['CURRENCY']=CURRENCY
    context['PUSHER_IS_ENABLE']=PUSHER_IS_ENABLE

    return context
def DefaultContext(request,app_name='core',*args, **kwargs):
    context=CoreContext(request=request,app_name=app_name)
    return context


class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['pages']=BasicPageRepo(request=request).list(for_home=True)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class PageViews(View):
    def page(self,request,*args, **kwargs):
        page=BasicPageRepo(request).page(*args, **kwargs)        
        context=getContext(request)
        context['page']=page
        context['add_child_form']=AddPageForm()
        context['childs']=page.childs.all()
        return render(request,TEMPLATE_ROOT+"page.html",context)