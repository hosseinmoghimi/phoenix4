from .models import *

class ProfileRepo():
    def __init__(self,user):
        self.user=user
        self.my_profiles=Profile.objects.filter(user=user)
        if user.has_perm(APP_NAME+'.view_profile'):
            self.objects=Profile.objects
        else:
            self.objects=self.my_profiles
        try:
            self.me=self.my_profiles.filter(user=user).filter(current=True).first()
        except:
            return None
    def profile(self,pk):
        try:
            return self.objects.get(pk=pk)
        except:
            return None
    
