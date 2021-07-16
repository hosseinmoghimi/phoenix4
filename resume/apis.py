from rest_framework.views import APIView
from core.constants import FAILED,SUCCEED
from .forms import AddContactMessageForm
from .repo import ContactMessageRepo
from django.http import JsonResponse


class BasicApi(APIView):
    def add_contact_message(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_contact_message_form=AddContactMessageForm(request.POST)
            if add_contact_message_form.is_valid():
                resume_index_id=add_contact_message_form.cleaned_data['resume_index_id']
                full_name=add_contact_message_form.cleaned_data['full_name']
                email=add_contact_message_form.cleaned_data['email']
                mobile=add_contact_message_form.cleaned_data['mobile']
                subject=add_contact_message_form.cleaned_data['subject']
                message=add_contact_message_form.cleaned_data['message']
                app_name=add_contact_message_form.cleaned_data['app_name']
                contact_message=ContactMessageRepo(request=request,app_name=app_name).add(resume_index_id=resume_index_id,full_name=full_name,email=email,mobile=mobile,subject=subject,message=message)
                if contact_message is not None:
                    return JsonResponse({'result':SUCCEED})
        context['log']=log
        return JsonResponse(context)