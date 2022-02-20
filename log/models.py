from django.db import models
from django.shortcuts import reverse
from .apps import APP_NAME
from django.utils.translation import gettext as _
# Create your models here.
class Log(models.Model):
    title=models.CharField(_("title"), max_length=500)
    desciption=models.CharField(_("desciption"),null=True,blank=True, max_length=50000)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":log", kwargs={"pk": self.pk})
