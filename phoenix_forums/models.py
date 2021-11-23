from core.models import BasicPage
from .apps import APP_NAME
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from .settings import *
from utility.persian import PersianCalendar
from .enums import *
class ForumsPage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(ForumsPage,self).save(*args, **kwargs)


# Create your models here.
class Forum(ForumsPage):    
    def childs(self):
        return Forum.objects.filter(parent=self)
    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
    def save(self,*args, **kwargs):
        self.class_name='forum'
        return super(Forum,self).save(*args, **kwargs)


class Post(ForumsPage):    
    post_forum=models.ForeignKey("forum", verbose_name=_("forum"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Post")
    def save(self,*args, **kwargs):
        self.class_name='post'
        return super(Post,self).save(*args, **kwargs)

