from .models import *
from django.contrib.auth import login, logout, authenticate

class ProfileRepo():
    def __init__(self,user):
        self.user=user
        if user is None or not user.is_authenticated:
            self.my_profiles=[]
            self.me=None
            return
        self.my_profiles=Profile.objects.filter(user=user) 
        try:
            self.me=Profile.objects.filter(user=user).filter(current=True).first()
        except:
            for profile in self.my_profiles:
                profile.current=False
                profile.save()
            first_profile=self.my_profiles.first()
            if first_profile is not None:
                first_profile.current=True
                first_profile.save()
        if user.has_perm(APP_NAME+'.view_profile'):
            self.objects=Profile.objects
        else:
            self.objects=self.my_profiles
       
    def profile(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'profile_id' in kwargs:
            return self.objects.filter(pk=kwargs['profile_id']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    @classmethod
    def logout(self,request):
        logout(request=request)

    def login(self,request,username,password):
        user=authenticate(request=request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_authenticated:
                return request
        return None