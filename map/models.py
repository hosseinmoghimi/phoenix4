from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .settings import *
from .enums import *
class Location(models.Model):
    title=models.CharField(_("title"), max_length=100)
    latitude=models.CharField(_("latitude"), max_length=50)
    longitude=models.CharField(_("longitude"), max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    def get_link_to_map(self):
        return f'https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}'
    def get_link_to_map_tag(self):
        return f"""
            <a title="نمایش روی نقشه" target="_blank" href="{self.get_link_to_map()}">
                <span class="material-icons">
                    location_on
                    </span>
                
            </a>
        """
    class Meta:
        verbose_name = _("VehicleLocation")
        verbose_name_plural = _("VehicleLocations")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":location", kwargs={"pk": self.pk})
