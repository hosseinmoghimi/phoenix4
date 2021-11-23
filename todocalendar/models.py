from core.enums import ColorEnum
from django.db import models
from django.db.models.fields import CharField
from core.models import BasicPage as CoreBasicPage
from .apps import APP_NAME
from .enums import *
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from utility.persian import PersianCalendar
IMAGE_FOLDER=APP_NAME+"/images/"
from core.models import BasicPage

class CalendarPage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(CalendarPage,self).save(*args, **kwargs)


class Appointment(CalendarPage):
    appointment_date=models.DateTimeField(_("appointment_date"), auto_now=False, auto_now_add=False)    
    persons=models.ManyToManyField("authentication.profile",blank=True, verbose_name=_("persons"))
    location=models.CharField(_("location"),blank=True,null=True, max_length=50)
    # importance=models.IntegerField(_("اولویت"),default=1)
    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments") 
    def save(self,*args, **kwargs):
        self.class_name='appointment'
        return super(Appointment,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(APP_NAME+":appointment", kwargs={"appointment_id": self.pk})
