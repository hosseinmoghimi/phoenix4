from .models import *
from django.contrib.auth import login, logout, authenticate

class ProfileRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.me=None
        self.objects=None   
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'forced' in kwargs:
            self.objects = Profile.objects.all()
        elif self.user is not None and self.user and self.user.is_authenticated:
            self.objects = Profile.objects.filter(enabled=True)
            self.me = self.objects.filter(user=self.user).first()         
           
                  
       
    def profile(self,*args, **kwargs):
        pk=0
        if 'profile_id' in kwargs:
            pk=kwargs['profile_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()

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

        
    def change_profile_image(self,profile_id,image):
        profile=ProfileRepo(user=self.user).get(profile_id=profile_id)
        if profile is not None:
            profile.image_origin = image
            profile.save()
            return True
        return False
    

    def edit_profile(self,profile_id,first_name,last_name,mobile,slogan,address,bio,postal_code):
        user=self.user
        if user.is_authenticated:
            me=ProfileRepo(user=user).me
            if me.id==profile_id or me.user.has_perm(APP_NAME+'.change_profile'):
                edited_profile=self.objects.get(pk=profile_id)
                
                if edited_profile is not None:
                    if edited_profile.user is not None:
                        edited_profile.user.first_name=first_name
                        edited_profile.user.last_name=last_name
                        edited_profile.user.save()


                    edited_profile.first_name=first_name
                    edited_profile.last_name=last_name
                    edited_profile.mobile=mobile
                    edited_profile.slogan=slogan
                    edited_profile.bio=bio
                    edited_profile.address=address
                    edited_profile.postal_code=postal_code
                    
                    edited_profile.save()
                    return edited_profile
        return None
    