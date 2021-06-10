from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models
from .enums import ProfileStatusEnum
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.conf import settings
from .apps import APP_NAME
IMAGE_FOLDER=APP_NAME+"/images/"

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
    mobile=models.CharField(_("mobile"),null=True,blank=True, max_length=50)
    bio=models.CharField(_("bio"),null=True,blank=True, max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    image_origin=models.ImageField(_("image"),null=True,blank=True, upload_to=IMAGE_FOLDER+"profile/", height_field=None, width_field=None, max_length=None)
    enabled=models.BooleanField(_("enabled"),default=True)
    @property
    def first_name(self):
        return self.user.first_name
    @property
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+APP_NAME+"/images/default-avatar.png"
    @property
    def last_name(self):
        return self.user.last_name
    @property
    def name(self):
        if self.user is not None:
            name=""
            if not (self.user.first_name is None or self.user.first_name==""):
                name=self.user.first_name+" "
                
            if not (self.user.last_name is None or self.user.last_name==""):
                name+=self.user.last_name+" "
            if not name=="":    
                return name
            else:
                return self.user.username
        
        else:
            return "profile "+str(self.pk)

    
    

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":profile", kwargs={"pk": self.pk})

    def get_absolute_url2(self):
        return reverse(APP_NAME+":profile2", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/profile/{self.pk}/change/"


class ProfileContact(models.Model):

    profile=models.ForeignKey("profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    value=models.CharField(_("value"), max_length=50)
    class Meta:
        verbose_name = _("ProfileContact")
        verbose_name_plural = _("ProfileContacts")

    def __str__(self):
        return f"{str(self.profile)} : {self.name} : {self.value}"
