# Create your models here.
from core.models import BasicPage
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

from core.settings import ADMIN_URL, STATIC_URL
from .apps import APP_NAME
from utility.persian import PersianCalendar
from django.utils.translation import gettext as _
from .settings import *
from .enums import *
class SchoolPage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(SchoolPage,self).save(*args, **kwargs)


class School(models.Model):
    class_name="school"
    title=models.CharField(_("نام مدرسه"), max_length=100)
    

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """

