from core.settings import ADMIN_URL, MEDIA_URL
from django.db import models
from django.shortcuts import reverse
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext as _
from utility.persian import PersianCalendar
from .apps import APP_NAME
IMAGE_FOLDER=APP_NAME+'/img/'
# Create your models here.
class Stock(models.Model):
    profile=models.ForeignKey("authentication.profile", related_name="stock_set",verbose_name=_("profile"), on_delete=models.CASCADE)
    agent=models.ForeignKey("authentication.profile", related_name="stock_agent_set",verbose_name=_("agent"), on_delete=models.CASCADE)
    stock1=models.IntegerField(_("stock1"),default=0)   
    stock2=models.IntegerField(_("stock2"),default=0)   
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now=True, auto_now_add=False)
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/stock/{self.pk}/change/"
    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":stock", kwargs={"pk": self.pk})



class Payment(models.Model):
    stock=models.ForeignKey("stock", verbose_name=_("stock"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    value=models.IntegerField(_("value"),default=0)
    image=models.ImageField(_("image"),null=True,blank=True, upload_to=IMAGE_FOLDER+"Payment", max_length=100)
    

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f'{self.stock.profile} : {self.name} : {self.value}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":payment", kwargs={"pk": self.pk})


class Document(models.Model):
    stock=models.ForeignKey("stock", verbose_name=_("stock"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    file=models.FileField(_("file"),null=True,blank=True, upload_to=IMAGE_FOLDER+"Document", max_length=100)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name="document"
    def get_download_url(self):
        return reverse(APP_NAME+":get_download_response",kwargs={'pk':self.pk})
    def get_image(self):
        if self.file is not None:
            return MEDIA_URL+str(self.file)
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self):
        return f'{self.stock.profile} : {self.title}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":document", kwargs={"pk": self.pk})
