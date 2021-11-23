from django.db import models
from django.db.models import Sum
from .apps import APP_NAME
from .enums import *
from core.models import BasicPage as CoreBasicPage
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from utility.persian import PersianCalendar

class HsePage(CoreBasicPage):
    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""

    class Meta:
        verbose_name = _("TaxPage")
        verbose_name_plural = _("TaxPages")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(HsePage, self).save(*args, **kwargs)

class Blog(HsePage):
    class_name='blog'
    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
 
    def save(self,*args, **kwargs):
        self.class_name='blog'
        return super(Blog,self).save(*args, **kwargs)
