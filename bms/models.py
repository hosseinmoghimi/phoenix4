from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import reverse
# Create your models here.

class Relay(models.Model):
    name=models.CharField(_("name"), max_length=50)

    

    class Meta:
        verbose_name = _("Relay")
        verbose_name_plural = _("Relays")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Relay_detail", kwargs={"pk": self.pk})
