from authentication.forms import EditProfileForm,UploadProfileImageForm
from django.http.response import JsonResponse
from rest_framework.views import APIView
from .repo import *
from core.constants import SUCCEED,FAILED

class ProfileApi(APIView):
    

    def edit_profile(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log+=1
            edit_profile_form=EditProfileForm(request.POST)
            if edit_profile_form.is_valid():
                log+=1                
                profile_id=edit_profile_form.cleaned_data['profile_id']
                first_name=edit_profile_form.cleaned_data['first_name']
                last_name=edit_profile_form.cleaned_data['last_name']
                email=edit_profile_form.cleaned_data['email']
                bio=edit_profile_form.cleaned_data['bio']
                mobile=edit_profile_form.cleaned_data['mobile']
                address=edit_profile_form.cleaned_data['address']
                result=ProfileRepo(request=request).edit_profile(profile_id=profile_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                bio=bio,
                mobile=mobile,
                address=address,
                )
                if result:
                    context['result']=SUCCEED

        context['log']=log
        return JsonResponse(context)