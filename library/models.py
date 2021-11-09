from django.db import models
from django.db.models import Sum
from .apps import APP_NAME
from .enums import *
from core.models import BasicPage as CoreBasicPage
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from utility.persian import PersianCalendar

class LibraryPage(CoreBasicPage):
    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""

    class Meta:
        verbose_name = _("TaxPage")
        verbose_name_plural = _("TaxPages")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(LibraryPage, self).save(*args, **kwargs)

class Book(LibraryPage):
    price=models.IntegerField(_("price"))
    year=models.IntegerField(_("year"))
    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
 
    def save(self,*args, **kwargs):
        self.class_name='book'
        return super(Book,self).save(*args, **kwargs)
