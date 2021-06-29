from core.models import BasicPage
from .apps import APP_NAME
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from .settings import *
from utility.persian import PersianCalendar
from .enums import *
class MessengerPage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(MessengerPage,self).save(*args, **kwargs)


class Message(MessengerPage):
    # forum=
    read=models.BooleanField(_("read?"),default=False)
    draft=models.BooleanField(_("draft?"),default=True)
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    # def __str__(self):
    #     return self.title
    def save(self,*args, **kwargs):
        self.class_name='message'
        return super(Message,self).save(*args, **kwargs)
    # def get_absolute_url(self):
    #     return reverse(APP_NAME+":message", kwargs={"pk": self.pk})

    # def get_edit_url(self):
    #     return f"{ADMIN_URL}{APP_NAME}/message/{self.pk}/change/"

