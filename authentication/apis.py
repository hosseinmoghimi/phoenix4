import re
from authentication.forms import AddProfileForm, EditProfileForm, AddMembershipRequestForm, HandleMembershipRequestForm, RegisterForm,UploadProfileImageForm
from django.http.response import JsonResponse
from rest_framework.views import APIView

from authentication.serializers import MembershipRequestSerializer, ProfileSerializer
from .repo import *
from core.constants import SUCCEED,FAILED

class MembershipRequestApi(APIView):
    def handle_membership_request(self,request,*args, **kwargs):
        context={'result':FAILED}
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        log=1
        if request.method=='POST':
            log=2
            fm=HandleMembershipRequestForm(request.POST)
            if fm.is_valid():
                log=3              
                # profile_id=edit_profile_form.cleaned_data['profile_id']
                membership_request_id=fm.cleaned_data['membership_request_id']
                membership_request=MembershipRequestRepo(request=request).handle_membership_request(membership_request_id=membership_request_id)
                if membership_request is not None:
                    context['membership_request']=MembershipRequestSerializer(membership_request).data
                    context['result']=SUCCEED

        context['log']=log
        return JsonResponse(context)    



    

    def add_membership_request(self,request,*args, **kwargs):
        context={'result':FAILED}
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        log=1
        if request.method=='POST':
            log=2
            fm=AddMembershipRequestForm(request.POST)
            if fm.is_valid():
                log=3              
                # profile_id=edit_profile_form.cleaned_data['profile_id']
                mobile=fm.cleaned_data['mobile']
                app_name=fm.cleaned_data['app_name']
                membership_request=MembershipRequestRepo(request=request).add_request(mobile=mobile,app_name=app_name)
                if membership_request is not None:
                    context['result']=SUCCEED
                    context['membership_request']=MembershipRequestSerializer(membership_request).data

        context['log']=log
        return JsonResponse(context)    


class ProfileApi(APIView):
    

    def edit_profile(self,request,*args, **kwargs):
        context={'result':FAILED}
        profile_id=0
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        log=1
        if request.method=='POST':
            log+=1
            edit_profile_form=EditProfileForm(request.POST)
            if edit_profile_form.is_valid():
                log+=1                
                # profile_id=edit_profile_form.cleaned_data['profile_id']
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

    def add_profile(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log+=1
            add_profile_form=AddProfileForm(request.POST)
            if add_profile_form.is_valid():
                log+=1                
                # profile_id=edit_profile_form.cleaned_data['profile_id']
                username=add_profile_form.cleaned_data['username']
                password=add_profile_form.cleaned_data['password']
                first_name=add_profile_form.cleaned_data['first_name']
                last_name=add_profile_form.cleaned_data['last_name']
                email=add_profile_form.cleaned_data['email']
                bio=add_profile_form.cleaned_data['bio']
                mobile=add_profile_form.cleaned_data['mobile']
                address=add_profile_form.cleaned_data['address']
                (result,profile,message)=ProfileRepo(request=request).add_profile(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    bio=bio,
                    mobile=mobile,
                    address=address,
                )
                context['message']=message
                context['result']=result
                if result==SUCCEED and profile is not None:
                    context['profile']=ProfileSerializer(profile).data

        context['log']=log
        return JsonResponse(context)    


    def register_profile(self,request,*args, **kwargs):
        context={'result':FAILED}
        log=1
        if request.method=='POST':
            log=2
            register_form=RegisterForm(request.POST)
            if register_form.is_valid():
                log=3
                first_name=register_form.cleaned_data['first_name']
                last_name=register_form.cleaned_data['last_name']
                bio=register_form.cleaned_data['bio']
                mobile=register_form.cleaned_data['mobile']
                email=register_form.cleaned_data['email']
                address=register_form.cleaned_data['address']
                (profile,result,message)=ProfileRepo(request=request).register(
                    first_name=first_name,
                    last_name=last_name,
                    bio=bio,
                    mobile=mobile,
                    address=address,
                    email=email,
                )
                context['result']=result
                context['message']=message
                
        context['log']=log
        return JsonResponse(context)