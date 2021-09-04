from .forms import AddPageForm
from web.forms import AddContactMessageForm
from rest_framework.views import APIView
from .serializers import *
from django.http import JsonResponse
from core.constants import SUCCEED,FAILED
from web.repo import BlogRepo, ContactMessageRepo
class BasicApi(APIView):
    def add_blog(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_page_form=AddPageForm(request.POST)
            if add_page_form.is_valid():
                title=add_page_form.cleaned_data['title']
                for_home=add_page_form.cleaned_data['for_home']
              
                blog=BlogRepo(request=request).add_blog(title=title,for_home=for_home)
                if blog is not None:
                    context['blog']=BlogSerializer(blog).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    def add_contact_message(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_contact_message_form=AddContactMessageForm(request.POST)
            if add_contact_message_form.is_valid():
                full_name=add_contact_message_form.cleaned_data['full_name']
                email=add_contact_message_form.cleaned_data['email']
                mobile=add_contact_message_form.cleaned_data['mobile']
                subject=add_contact_message_form.cleaned_data['subject']
                message=add_contact_message_form.cleaned_data['message']
                app_name=add_contact_message_form.cleaned_data['app_name']
                contact_message=ContactMessageRepo(request=request,app_name=app_name).add(full_name=full_name,email=email,mobile=mobile,subject=subject,message=message)
                if contact_message is not None:
                    return JsonResponse({'result':SUCCEED})
        context['log']=log
        return JsonResponse(context)