from django.db import models
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

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse("Stock_detail", kwargs={"pk": self.pk})
