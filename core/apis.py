from core.serializers import BasicPageSerializer, PageCommentSerializer, PageDocumentSerializer, PageImageSerializer, PageLinkSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import BasicPageRepo, DocumentRepo, PageCommentRepo, PageImageRepo, PageLinkRepo
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
    def add_page_comment(self,request,*args, **kwargs):
        log=1
        context={}
        context['result']=FAILED
        if request.method=='POST':
            log+=1
            add_page_comment_form=AddPageCommentForm(request.POST)
            if add_page_comment_form.is_valid():
                log+=1
                comment=add_page_comment_form.cleaned_data['comment']
                page_id=add_page_comment_form.cleaned_data['page_id']
                page_comment=PageCommentRepo(request=request).add_comment(comment=comment,page_id=page_id)
                if page_comment is not None:
                    context['page_comment']=PageCommentSerializer(page_comment).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def delete_page_comment(self,request,*args, **kwargs):
        log=1
        context={}
        context['result']=FAILED
        if request.method=='POST':
            log+=1
            delete_page_comment_form=DeletePageCommentForm(request.POST)
            if delete_page_comment_form.is_valid():
                log+=1
                page_comment_id=delete_page_comment_form.cleaned_data['page_comment_id']
                done=PageCommentRepo(request=request).delete_comment(page_comment_id=page_comment_id)
                if done:
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
                if page_document is not None:
                    context['page_document']=PageDocumentSerializer(page_document,context={'request':request}).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    def add_page_image(self,request,*args, **kwargs):
        log=1
        context={}
        context['result']=FAILED
        if request.method=='POST':
            log+=1
            add_page_image_form=AddPageImageForm(request.POST,request.FILES)
            if add_page_image_form.is_valid():
                log+=1
                title=add_page_image_form.cleaned_data['title']
                page_id=add_page_image_form.cleaned_data['page_id']
                image=request.FILES['image']              
                page_image=PageImageRepo(request=request).add_page_image(title=title,image=image,page_id=page_id)
                if page_image is not None:
                    context['page_image']=PageImageSerializer(page_image,context={'request':request}).data
        context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
