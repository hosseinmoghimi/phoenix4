from core.settings import SITE_URL
from django.shortcuts import render,redirect
from .repo import *
from .forms import *
from django.views import View
from core.views import CoreContext

TEMPLATE_ROOT="authentication/"
def getContext(request):
    context=CoreContext(request=request,app_name=APP_NAME)
    return context
class BasicViews(View):
    def home(self,request,*args, **kwargs):
        context=getContext(request)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class ProfileViews(View):
    def profile(self,request,*args, **kwargs):
        context=getContext(request)
        context['layout']="base-layout.html"
        selected_profile=ProfileRepo(user=request.user)
        if 'profile_id' in kwargs:
            selected_profile=ProfileRepo(request=request).profile(pk=kwargs['profile_id'])
        if 'pk' in kwargs:
            selected_profile=ProfileRepo(request=request).profile(pk=kwargs['pk'])
        context['selected_profile']=selected_profile
        return render(request,TEMPLATE_ROOT+"profile.html",context)
    def profile2(self,request,*args, **kwargs):
        context=getContext(request)
        context['layout']="base-layout.html"
        return render(request,TEMPLATE_ROOT+"profile2.html",context)
class AuthenticationViews(View):
    def login(self,request,*args, **kwargs):
        if request.method=='POST':
            login_form=LoginForm(request.POST)
            if login_form.is_valid():
                username=login_form.cleaned_data['username']

                password=login_form.cleaned_data['password']
                back_url=login_form.cleaned_data['back_url']
                if back_url is None or not back_url:
                    back_url=SITE_URL
                request1=ProfileRepo(user=None).login(request=request,username=username,password=password)
                if request1 is not None and request1.user is not None and request1.user.is_authenticated :
                    # print(back_url)
                    # print(100*'#')
                    # Token.objects.filter(user=request1.user).delete()
                    # Token.objects.create(user=request1.user)
                    return redirect(back_url)
                else:   
                    context=getContext(request=request)
                    context['message']='نام کاربری و کلمه عبور صحیح نمی باشد.'
                    context['login_form']=LoginForm()
                    context['search_form']=None
                    context['register_form']=RegisterForm()
                    context['back_url']=back_url
                    context['reset_password_form']=ResetPasswordForm()
                    return render(request,TEMPLATE_ROOT+'login.html',context)
        else:
            context=getContext(request)
            return render(request,TEMPLATE_ROOT+"login.html",context)
    def logout(self,request):
        ProfileRepo.logout(request)
        return redirect(reverse('authentication:login'))