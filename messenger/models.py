from django.db.models.base import Model
from django.db.models.fields import CharField
from core.models import BasicPage
from .apps import APP_NAME
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from .settings import *
from utility.persian import PersianCalendar
from .enums import *
IMAGE_FOLDER=APP_NAME+"/images/"


class MessengerPage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(MessengerPage,self).save(*args, **kwargs)


class Message(models.Model):
    title=models.CharField(_("title"), max_length=50)
    body=models.CharField(_("body"), max_length=50)
    channel=models.ForeignKey("channel", verbose_name=_(""), on_delete=models.CASCADE)
    event=models.CharField(_("event"), max_length=50)
    # read=models.BooleanField(_("read?"),default=False)
    # draft=models.BooleanField(_("draft?"),default=True)
    date_send=models.DateTimeField(_("date send"), auto_now=False, auto_now_add=True)
    sender=models.ForeignKey("authentication.profile", verbose_name=_("sender"), on_delete=models.CASCADE)
    class_name="message"
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
    def perisan_date_send(self):
        return PersianCalendar().from_gregorian(self.date_send)
    # def __str__(self):
    #     return self.title
    # def save(self,*args, **kwargs):
    #     self.class_name='message'
    #     return super(Message,self).save(*args, **kwargs)
    # def get_absolute_url(self):
    #     return reverse(APP_NAME+":message", kwargs={"pk": self.pk})

    # def get_edit_url(self):
    #     return f"{ADMIN_URL}{APP_NAME}/message/{self.pk}/change/"



class Channel(models.Model):
    title=models.CharField(_("title"), max_length=100)
    image_origin=models.ImageField(_("image"),null=True,blank=True, upload_to=IMAGE_FOLDER+"channel/", height_field=None, width_field=None, max_length=None)
    description=CharField(_("description"),null=True,blank=True,max_length=500)
    channel_name=models.CharField(verbose_name='channel_name',max_length=20) 
    
    app_id =models.CharField(verbose_name='app_id',max_length=20) 
    key = models.CharField(verbose_name='key',max_length=50)
    secret = models.CharField(verbose_name='secret',max_length=50)
    cluster =models.CharField(verbose_name='cluster',max_length=20,default='us2')
    class_name="channel"
    
    def member_count(self):
        member_count=0
        member_count=len(self.member_set.all())
        return member_count
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    @property
    def name(self):
        return self.channel_name
    def __str__(self):
        return self.channel_name+' : '+str(self.key)

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
    def get_absolute_url(self):
        return reverse(APP_NAME+":channel", kwargs={"pk": self.pk})
    
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        else:
            return STATIC_URL+APP_NAME+"/img/channel.png"

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

    def __str__(self):
        return self.channel_name


class Member(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    channel=models.ForeignKey("channel", verbose_name=_("channel"), on_delete=models.CASCADE)
    event=models.CharField(_("event"),default="DEFAULT", max_length=50)
    date_join=models.DateTimeField(_("date join"), auto_now=False, auto_now_add=False)
    
    class_name="member"
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")

    def __str__(self):
        return f"""{self.event} {self.profile.name}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":member", kwargs={"pk": self.pk})
