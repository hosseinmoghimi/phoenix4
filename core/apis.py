from core.serializers import BasicPageSerializer, PageDocumentSerializer, PageLinkSerializer
from core.models import BasicPage
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import BasicPageRepo, DocumentRepo, PageLinkRepo
from .constants import SUCCEED,FAILED
class BasicApi(APIView):
    def add_page(self,request,*args, **kwargs):
        log=1
        context={}
        context['result']=FAILED
        if request.method=='POST':
            log+=1
            add_page_form=AddPageForm(request.POST)
            if add_page_form.is_valid():
                log+=1
                title=add_page_form.cleaned_data['title']
                parent_id=add_page_form.cleaned_data['parent_id']
                page=BasicPageRepo(request).add_page(title=title,parent_id=parent_id)
                if page is not None:
                    context['page']=BasicPageSerializer(page).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def add_page_link(self,request,*args, **kwargs):
        log=1
        context={}
        context['result']=FAILED
        if request.method=='POST':
            log+=1
            add_page_link_form=AddPageLinkForm(request.POST)
            if add_page_link_form.is_valid():
                log+=1
                title=add_page_link_form.cleaned_data['title']
                page_id=add_page_link_form.cleaned_data['page_id']
                url=add_page_link_form.cleaned_data['url']
                page_link=PageLinkRepo(request=request).add_page_link(title=title,url=url,page_id=page_id)
                if page_link is not None:
                    context['page_link']=PageLinkSerializer(page_link).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def add_page_document(self,request,*args, **kwargs):
        log=1
        context={}
        context['result']=FAILED
        if request.method=='POST':
            log+=1
            add_page_document_form=AddPageDocumentForm(request.POST,request.FILES)
            if add_page_document_form.is_valid():
                log+=1
                title=add_page_document_form.cleaned_data['title']
                page_id=add_page_document_form.cleaned_data['page_id']
                file=request.FILES['file1']              
                page_document=DocumentRepo(request=request).add_page_document(title=title,file=file,page_id=page_id)
                print(page_document)
                print(100*"#23643#")
                if page_document is not None:
                    context['page_document']=PageDocumentSerializer(page_document,context={'request':request}).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
