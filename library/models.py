from django.db import models
from django.db.models import Sum
from .apps import APP_NAME
from .enums import *
from core.models import BasicPage as CoreBasicPage
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from utility.persian import PersianCalendar

class Admin_Model():
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})


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
    shelf=models.CharField(_("shelf"),null=True,blank=True, max_length=50)
    row=models.CharField(_("row"),null=True,blank=True, max_length=50)
    col=models.CharField(_("col"),null=True,blank=True, max_length=50)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
 
    def save(self,*args, **kwargs):
        self.class_name='book'
        return super(Book,self).save(*args, **kwargs)

class Member(models.Model,Admin_Model):
    profile=models.ForeignKey("authentication.profile",related_name="library_member_set", verbose_name=_("profile"), on_delete=models.CASCADE)
    membership_started=models.DateTimeField(_("شروع عضویت"),null=True,blank=True, auto_now=False, auto_now_add=False)
    membership_ended=models.DateTimeField(_("پایان عضویت"),null=True,blank=True, auto_now=False, auto_now_add=False)
    level=models.CharField(_("level"),choices=MemberShipLevelEnum.choices,default=MemberShipLevelEnum.REGULAR, max_length=50)
    class_name="member"
    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
    def color(self):
        if self.level==MemberShipLevelEnum.MASTER:
            return 'danger'
        return 'primary'
    def __str__(self):
        return self.profile.name

    def persian_membership_started(self):
        return PersianCalendar().from_gregorian(self.membership_started)[:10]



    def persian_membership_ended(self):
        return PersianCalendar().from_gregorian(self.membership_ended)[:10]



class Lend(models.Model,Admin_Model):
    member=models.ForeignKey("member", verbose_name=_("member"), on_delete=models.CASCADE)
    book=models.ForeignKey("book", verbose_name=_("book"), on_delete=models.CASCADE)
    date_lended=models.DateTimeField(_("تاریخ امانت"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_returned=models.DateTimeField(_("تاریخ برگشت"),null=True,blank=True, auto_now=False, auto_now_add=False)
    description=models.CharField(_("description"),null=True,blank=True, max_length=5000)
    class_name="lend"
    class Meta:
        verbose_name = _("Lend")
        verbose_name_plural = _("Lends")
    def persian_date_lended(self):
        return PersianCalendar().from_gregorian(self.date_lended)[:10]
    def persian_date_returned(self):
        return PersianCalendar().from_gregorian(self.date_returned)[:10]
    def __str__(self):
        return f"{str(self.member)} => {str(self.book)}"
    


    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})
