import json
from core.serializers import BasicPageSerializer, PageCommentSerializer
from django.utils import timezone
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
def CoreContext(request,*args, **kwargs):
    context={}
    app_name='core'
    if 'app_name' in kwargs:
        app_name=kwargs['app_name']
    context['user']=request.user
    context['profile']=ProfileRepo(user=request.user).me
    context['APP_NAME']=app_name
    context['current_datetime']=PersianCalendar().from_gregorian(timezone.now())
    context['current_date']=PersianCalendar().from_gregorian(timezone.now())[:10]
    context[app_name+'_sidebar']=True
    context['DEBUG']=DEBUG
    context['ADMIN_URL']=ADMIN_URL
    context['MEDIA_URL']=MEDIA_URL
    context['SITE_URL']=SITE_URL
    context['CURRENCY']=CURRENCY
    context['PUSHER_IS_ENABLE']=PUSHER_IS_ENABLE

    return context
def PageContext(request,page):
    if page is None:
        return {}
    context={}
    context['page']=page
    context['parent_id']=page.id

    if request.user.has_perm(APP_NAME+".add_pagelink"):
        context['add_page_link_form']=AddPageLinkForm()

    if request.user.has_perm(APP_NAME+".add_pagedocument"):
        context['add_page_document_form']=AddPageDocumentForm()
    page_comments=page.pagecomment_set.all()
    context['page_comments']=page_comments
    page_comments_s=json.dumps(PageCommentSerializer(page_comments,many=True).data)
    context['page_comments_s']=page_comments_s
    return context
def getContext(request):
    context=DefaultContext(request=request,app_name=APP_NAME)
    context["layout_root"]=TEMPLATE_ROOT+"/layout.html"
    context["admin_utility"]=AdminUtility(request=request)
    return context
# Create your views here.
def DefaultContext(request,app_name='core',*args, **kwargs):
    context=CoreContext(request=request,app_name=app_name)
    return context


class MessageView(View):
    def __init__(response,*args, **kwargs):
        response.links=[]
        response.message_text_html=None
        if 'message_html' in kwargs:
            response.message_html=kwargs['message_html']
        response.message_color='warning'
        response.has_home_link=True
        response.header_color="rose"
        response.message_icon=''
        response.header_icon='<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        response.message_text=None
        response.header_text=None
    def response(self,request,*args, **kwargs):
        return self.show(request=request)
    def show(self,request,*args, **kwargs):
        context=CoreContext(request,*args, **kwargs)
        if self.header_text is None:
            self.header_text='خطا'
        if self.message_text is None:
            self.message_text='متاسفانه خطایی رخ داده است.'
        if self.has_home_link:
            btn_home=Link(url=(SITE_URL),
            color=ColorEnum.SUCCESS+' btn-round',
            icon_material=IconsEnum.home,
            title='خانه',name='ssss',new_tab=False)
            self.links.append(btn_home)
        context['links']=self.links

        context['header_text']=self.header_text
        context['header_color']=self.header_color
        context['header_icon']=self.header_icon

        context['message_color']=self.message_color
        context['message_icon']=self.message_icon
        context['message_text']=self.message_text
        context['message_html']=self.message_html

        context['search_form']=None
        return render(request,TEMPLATE_ROOT+'error.html',context)



class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        context['pages']=BasicPageRepo(request=request).list(for_home=True)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class PageViews(View):
    def page_chart(self, request, *args, **kwargs):
        context = getContext(request)
        if 'pk' in kwargs and kwargs['pk']>0:
            pk=kwargs['pk']
        else:
            pk=0

        page=(BasicPageRepo(request=request).page(pk=pk))
        pages=page.all_sub_pages()
        pages_s = BasicPageSerializer(pages, many=True).data
        context['pages_s'] = json.dumps(pages_s)
        return render(request, "dashboard/pages-chart.html", context)

    def download(self,request,pk):
        if request.user.is_authenticated and request.user.has_perm("core.change_document"):
            document=DocumentRepo(user=request.user).document(document_id=pk)
            return document.download_response()
        
        document=DocumentRepo(user=request.user).document(pk=pk)
        if document is None:
            raise Http404


        if self.access(request=request,pk=pk) and document is not None:
            return document.download_response()
        message_view= MessageView()
        message_view.links=[]
        message_view.links.append(Link(title='تلاش مجدد',icon_color="warning",icon_material="apartment",url=document.get_download_url()))
        message_view.message_color='warning'
        message_view.has_home_link=True
        message_view.header_color="rose"
        message_view.message_icon=''
        message_view.header_icon='<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        message_view.message_text='مجوز شما برای دسترسی به این صفحه مجاز نمی باشد.'
        message_view.header_text='دسترسی غیر مجاز'

        return message_view.response(request)

    def access(self,request,pk):
        return True
        document=DocumentRepo(user=request.user).document(pk=pk)
        self.me=ProfileRepo(user=request.user).me
        if self.me is not None and document.page in self.me.my_pages().all():
            return True
        if request.user.has_perm(APP_NAME+'.view_document'):
            return True
        if document.page.app_name=='web':
            return True
        return False

    def page(self,request,*args, **kwargs):
        page=BasicPageRepo(request).page(*args, **kwargs)        
        context=getContext(request)
        context['page']=page
        context['add_child_form']=AddPageForm()
        context['childs']=page.childs.all()
        return render(request,TEMPLATE_ROOT+"page.html",context)