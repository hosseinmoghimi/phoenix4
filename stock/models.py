from django.db import models
from django.utils.translation import gettext as _
from utility.persian import PersianCalendar
from .apps import APP_NAME
IMAGE_FOLDER=APP_NAME+'/img/'
# Create your models here.
class Stock(models.Model):


    

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Stock_detail", kwargs={"pk": self.pk})
