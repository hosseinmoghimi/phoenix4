from .models import *
from django.contrib.auth import login, logout, authenticate

class ProfileRepo():
    def __init__(self,user=None):
        self.me=None
        self.objects=None   
        if user is not None and user and user.is_authenticated:
            self.user = user
            self.objects = Profile.objects.filter(enabled=True)
            self.me = self.objects.filter(user=user).first()         
           
                  
       
    def profile(self,*args, **kwargs):
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'profile_id' in kwargs:
            pk=kwargs['profile_id']
        if 'id' in kwargs:
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
            me=ProfileRepo(user).me
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
    