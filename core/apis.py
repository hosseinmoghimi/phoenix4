from core.serializers import BasicPageSerializer, PageCommentSerializer, PageDocumentSerializer, PageImageSerializer, PageLinkSerializer, ParameterSerializer, TagSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import BasicPageRepo, DocumentRepo, PageCommentRepo, PageImageRepo, PageLinkRepo, ParameterRepo, TagRepo
from .constants import SUCCEED, FAILED


class BasicApi(APIView):
    def change_parameter(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            change_parameter_form = ChangeParameterForm(request.POST)
            if change_parameter_form.is_valid():
                log += 1
                
                parameter_id = change_parameter_form.cleaned_data['parameter_id']
                app_name = change_parameter_form.cleaned_data['app_name']
                parameter_name = change_parameter_form.cleaned_data['parameter_name']
                parameter_value = change_parameter_form.cleaned_data['parameter_value']
                
                parameter = ParameterRepo(request=request).change_parameter(
                    parameter_id=parameter_id,
                    app_name=app_name,
                    parameter_name=parameter_name,
                    parameter_value=parameter_value,
                    )
                if parameter is not None:
                    context['parameter'] = ParameterSerializer(parameter).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    def add_page(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_form = AddPageForm(request.POST)
            if add_page_form.is_valid():
                log += 1
                title = add_page_form.cleaned_data['title']
                parent_id = add_page_form.cleaned_data['parent_id']
                page = BasicPageRepo(request).add_page(
                    title=title, parent_id=parent_id)
                if page is not None:
                    context['page'] = BasicPageSerializer(page).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def add_related_page(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log = 2
            add_related_page_form = AddRelatedPageForm(request.POST)
            if add_related_page_form.is_valid():
                log = 3
                page_id = add_related_page_form.cleaned_data['page_id']
                related_page_id = add_related_page_form.cleaned_data['related_page_id']
                bidirectional = add_related_page_form.cleaned_data['bidirectional']
                add_or_remove = add_related_page_form.cleaned_data['add_or_remove']
                related_page = BasicPageRepo(request=request).add_related_page(add_or_remove=add_or_remove,page_id=page_id, bidirectional=bidirectional, related_page_id=related_page_id)
                if related_page is not None:
                    log = 4
                    context['related_page'] = BasicPageSerializer(related_page).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def add_page_tag(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log = 2
            add_page_tag_form = AddPageTagForm(request.POST)
            if add_page_tag_form.is_valid():
                log = 3
                page_id = add_page_tag_form.cleaned_data['page_id']
                title = add_page_tag_form.cleaned_data['title']
                tag = TagRepo(request=request).add_page_tag(page_id=page_id, title=title)
                if tag is not None:
                    log = 4
                    context['tag'] = TagSerializer(tag).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def remove_page_tag(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log = 2
            remove_page_tag_form = RemovePageTagForm(request.POST)
            if remove_page_tag_form.is_valid():
                log = 3
                page_id = remove_page_tag_form.cleaned_data['page_id']
                tag_id = remove_page_tag_form.cleaned_data['tag_id']
                res= TagRepo(request=request).remove_page_tag(page_id=page_id, tag_id=tag_id)
                if res:
                    log = 4
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    def add_page_comment(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_comment_form = AddPageCommentForm(request.POST)
            if add_page_comment_form.is_valid():
                log += 1
                comment = add_page_comment_form.cleaned_data['comment']
                page_id = add_page_comment_form.cleaned_data['page_id']
                comment1=comment.splitlines()
                comment=""
                for line in comment1:
                    comment=comment+line+"<br>"
                page_comment = PageCommentRepo(request=request).add_comment(
                    comment=comment, page_id=page_id)
                if page_comment is not None:
                    context['page_comment'] = PageCommentSerializer(
                        page_comment).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def delete_page_comment(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            delete_page_comment_form = DeletePageCommentForm(request.POST)
            if delete_page_comment_form.is_valid():
                log += 1
                page_comment_id = delete_page_comment_form.cleaned_data['page_comment_id']
                done = PageCommentRepo(request=request).delete_comment(
                    page_comment_id=page_comment_id)
                if done:
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def add_page_link(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_link_form = AddPageLinkForm(request.POST)
            if add_page_link_form.is_valid():
                log += 1
                title = add_page_link_form.cleaned_data['title']
                page_id = add_page_link_form.cleaned_data['page_id']
                url = add_page_link_form.cleaned_data['url']
                page_link = PageLinkRepo(request=request).add_page_link(
                    title=title, url=url, page_id=page_id)
                if page_link is not None:
                    context['page_link'] = PageLinkSerializer(page_link).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def add_page_document(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_document_form = AddPageDocumentForm(
                request.POST, request.FILES)
            if add_page_document_form.is_valid():
                log += 1
                title = add_page_document_form.cleaned_data['title']
                page_id = add_page_document_form.cleaned_data['page_id']
                file = request.FILES['file1']
                page_document = DocumentRepo(request=request).add_page_document(
                    title=title, file=file, page_id=page_id)
                if page_document is not None:
                    context['page_document'] = PageDocumentSerializer(
                        page_document, context={'request': request}).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    def add_page_image(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_image_form = AddPageImageForm(request.POST, request.FILES)
            if add_page_image_form.is_valid():
                log += 1
                title = add_page_image_form.cleaned_data['title']
                page_id = add_page_image_form.cleaned_data['page_id']
                image = request.FILES['image']
                page_image = PageImageRepo(request=request).add_page_image(
                    title=title, image=image, page_id=page_id)
                if page_image is not None:
                    context['page_image'] = PageImageSerializer(
                        page_image, context={'request': request}).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
