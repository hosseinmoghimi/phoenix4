from django.db import models
from .enums import ProfileStatusEnum
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.conf import settings
from .apps import APP_NAME

from django.db.models.signals import post_save

def create_profile_receiver(sender,instance,created,*args, **kwargs):  
    if created:
        profile=Profile(user_id=instance.id)
        profile.save()

def save_profile_receiver(sender,instance,*args, **kwargs):    
    profile=instance.profile
    profile.save()
    # if profile.region is None:
    #     try:
    #         from core.models import Region
    #         profile.region=Region.objects.first()
    #         profile.save()
    #     except:
    #         pass
    # try:
    #     from market.models import Customer
    #     customers=Customer.objects.filter(profile=profile)
    #     if len(customers)==0:
    #         customer=Customer()
    #         customer.profile=profile
    #         customer.title=instance.first_name+" "+instance.last_name
    #         customer.save()
    # except:
    #     pass
    

post_save.connect(create_profile_receiver, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_profile_receiver, sender=settings.AUTH_USER_MODEL)





class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,null=True,blank=True)
    current=models.BooleanField(_("current"),default=True)
    @property
    def name(self):
        if self.user is not None:
            name=""
            if not self.user.first_name=="":
                name+=self.user.first_name+" "
                
            if not self.user.last_name=="":
                name+=self.user.last_name+" "
            if not name=="":    
                return name
        
        else:
            return "profile "+str(self.pk)

    

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":profile", kwargs={"pk": self.pk})


# class ProfileContact(models.Model):

#     profile=models.ForeignKey("profile", verbose_name=_("profile"), on_delete=models.CASCADE)
#     name=models.CharField(_("name"), max_length=50)
#     value=models.CharField(_("value"), max_length=50)
#     class Meta:
#         verbose_name = _("ProfileContact")
#         verbose_name_plural = _("ProfileContacts")

#     def __str__(self):
#         return f"""{self.profile.name} : {self.name} : {self.value}"""
