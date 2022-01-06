from datetime import datetime
from django.db import models
from core.models import BasicPage
from core.settings import ADMIN_URL 
from .apps import APP_NAME
from .enums import *
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from utility.persian import PersianCalendar
IMAGE_FOLDER = APP_NAME+"/images/"


class PostmanPage(BasicPage):
    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""

    class Meta:
        verbose_name = _("PostmanPage")
        verbose_name_plural = _("PostmanPages")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(PostmanPage, self).save(*args, **kwargs)


# Create your models here.

class Letter(PostmanPage):
    # sender=models.ForeignKey("authentication.profile", verbose_name=_("sender"),related_name="letters_send", on_delete=models.CASCADE)
    # receiver=models.ForeignKey("authentication.profile", verbose_name=_("receiver"),related_name="letters_received", on_delete=models.CASCADE)
    # sender=models.ForeignKey("projectmanager.organizationunit", verbose_name=_("sender"),related_name="letters_send", on_delete=models.CASCADE)
    # receiver=models.ForeignKey("projectmanager.organizationunit", verbose_name=_("receiver"),related_name="letters_received", on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Letter'
        verbose_name_plural = 'Letters'

    def save(self, *args, **kwargs):
        self.class_name = 'letter'
        return super(Letter, self).save(*args, **kwargs)


class LetterPosition(models.Model):
    letter=models.ForeignKey("letter", verbose_name=_("letter") , on_delete=models.CASCADE)
    sender=models.ForeignKey("projectmanager.organizationunit", verbose_name=_("sender"),related_name="letters_send", on_delete=models.CASCADE)
    receiver=models.ForeignKey("projectmanager.organizationunit", verbose_name=_("receiver"),related_name="letters_received", on_delete=models.CASCADE)
    date_sent=models.DateTimeField(_("تاریخ ارسال"), auto_now=False, auto_now_add=True)
    
    class Meta:
        verbose_name = 'LetterPosition'
        verbose_name_plural = 'LetterPositions'
 
    def persian_date_sent(self):
        return PersianCalendar().from_gregorian(self.date_sent)

    def __str__(self):
        return self.letter.title
 
class LetterSignature(models.Model):
    letter = models.ForeignKey("letter", verbose_name=_("letter"), on_delete=models.CASCADE)
    profile = models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.PROTECT)
    date_added = models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    description = models.CharField(_("description"), max_length=200)
    status = models.CharField(_("status"), choices=LetterStatusEnum.choices,default=LetterStatusEnum.DEFAULT, max_length=200)

    class_name = "lettersignature"

    class Meta:
        verbose_name = _("LetterSignature")
        verbose_name_plural = _("LetterSignatures")

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""
            <span class="badge badge-{self.get_status_color()}">{self.status}</span>
        """

    def __str__(self):
        return f"""{self.letter.title} : {self.profile.name} : {self.status} """
 
   
