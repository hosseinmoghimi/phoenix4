from rest_framework.fields import ImageField
from utility.persian import PersianCalendar
from django.db import models
from .apps import APP_NAME
from .enums import *
from .settings import *
from django.shortcuts import reverse
import requests
from django.utils.translation import gettext as _

IMAGE_FOLDER=APP_NAME+"/images/"
class Feeder(models.Model):
    name=models.CharField(_("name"), max_length=50)
    serial_no=models.CharField(_("serial_no"), max_length=50)
    ip=models.CharField(_("ip"),default="192.168.45.200", max_length=50)
    port=models.IntegerField("port",default=80)
    feeder_pin=models.CharField(_("feeder_pin"),default="09155323633@", max_length=50)
    is_protected=models.BooleanField(_("is_protected"),default=False)
    thumbnail_origin=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+"feeder/", height_field=None, width_field=None, max_length=None,null=True,blank=True)
    @property
    def pin(self):
        if self.is_protected:
            return ""
        return self.feeder_pin
    def get_edit_btn(self):
        return f"""
                  <a href="{self.get_edit_url()}" target="_blank" title="ویرایش فیدر {self.name}">
                      <i class="material-icons">settings</i>
                  </a>
        """
    class Meta:
        verbose_name = _("Feeder")
        verbose_name_plural = _("Feeders")
    def thumbnail(self):       
        if not self.thumbnail_origin:
            return CoreSettings.STATIC_URL+APP_NAME+"/room.png"
        else:
            return CoreSettings.MEDIA_URL+str(self.thumbnail_origin)
    def __str__(self):
        return self.name
    def get_edit_url(self):
        return f"{CoreSettings.ADMIN_URL}{APP_NAME}/feeder/{self.pk}/change/"

    def get_absolute_url(self):
        return reverse(APP_NAME+":feeder", kwargs={"pk": self.pk})



# 3-16-4-12
class Relay(models.Model):
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), on_delete=models.CASCADE)
    name=models.CharField(_("name"),max_length=50)
    enabled=models.BooleanField(_("enabled"),default=True)
    register=models.IntegerField(_("register"))#3-16-4-12
    current_state=models.BooleanField(_("state"),default=False)
    relay_pin=models.CharField(_("relay_pin"),default="09155323633@", max_length=50)
    class_name='relay'
    is_protected=models.BooleanField(_("protected"),default=False)
    @property
    def pin(self):
        if self.is_protected:
            return ""
        return self.relay_pin
    def get_edit_btn(self):
        return f"""
            <a title="ویرایش" href="{self.get_edit_url()}">
                <span class="material-icons text-warning">
                    edit
                </span>
            </a>
        """
    def get_edit_url(self):
        return f"""{CoreSettings.ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""
 

    class Meta:
        verbose_name = _("Relay")
        verbose_name_plural = _("Relays")

    def __str__(self):
        return f'{self.feeder.name} {self.name} =>[ {self.register} ] => {self.current_state}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":relay", kwargs={"pk": self.pk})

class Command(models.Model):
    relay=models.ForeignKey("relay", verbose_name=_("relay"), on_delete=models.CASCADE)
    iteration=models.IntegerField(_("iteration"),default=1)
    name=models.CharField(_("name"), max_length=50)
    value=models.CharField(_("value"), max_length=50)
    color=models.CharField(_("color"),choices=CoreEnums.ColorEnum.choices,default=CoreEnums.ColorEnum.SUCCESS, max_length=50)
    profiles=models.ManyToManyField("authentication.profile", verbose_name=_("profiles"))
    class Meta:
        verbose_name = _("Command")
        verbose_name_plural = _("Commands")

    def __str__(self):
        return f'{self.relay.feeder.name} => {self.relay.name} {self.name}'
    def persian_date_added(self):
        
        p=PersianCalendar().from_gregorian(self.date_added)
        e=self.date_added
        return f"""
            <span title="{e}">{p}</span>
        """
    def get_edit_btn(command):
        return f"""
        <a title="ویرایش" href="{command.get_edit_url()}">
                                    <i class="material-icons text-warning">
                                        settings
                                    </i>
                                </a>
        """
    def get_edit_url(self):
        return f"""{CoreSettings.ADMIN_URL}{APP_NAME}/command/{self.pk}/change/"""
    def get_absolute_url(self):
        return reverse(APP_NAME+":command", kwargs={"pk": self.pk})

class Log(models.Model):
    title=models.CharField(_("title"), max_length=50)
    profile=models.ForeignKey("authentication.profile",null=True,blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    relay=models.ForeignKey("relay", verbose_name=_("relay"), blank=True,null=True,on_delete=models.CASCADE)
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), blank=True,null=True,on_delete=models.CASCADE)
    command=models.ForeignKey("command", verbose_name=_("command"), blank=True,null=True,on_delete=models.CASCADE)
    scenario=models.ForeignKey("scenario", verbose_name=_("scenario"), blank=True,null=True,on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    succeed=models.BooleanField(_("succeed"),default=True)
    def persian_date_added(self):
        
        p=PersianCalendar().from_gregorian(self.date_added)
        e=self.date_added
        return f"""
            <span title="{e}">{p}</span>
        """
    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":log", kwargs={"pk": self.pk})

class Scenario(models.Model):
    name=models.CharField(_("name"), max_length=50)
    commands=models.ManyToManyField("command",blank=True, verbose_name=_("commands"))
    profiles=models.ManyToManyField("authentication.profile",blank=True, verbose_name=_("profiles"))
    is_protected=models.BooleanField(_("is_protected"),default=False)
    scenario_pin=models.CharField(_("pin"),default="09155323633@", max_length=50)
    color=models.CharField(_("color"),choices=CoreEnums.ColorEnum.choices,default=CoreEnums.ColorEnum.PRIMARY, max_length=50)
    @property
    def pin(self):
        if self.is_protected:
            return ""
        return self.scenario_pin
    def get_edit_btn(self):
        return f"""
                  <a href="{self.get_edit_url()}" target="_blank" title="ویرایش سناریوی {self.name}">
                      <i class="material-icons">settings</i>
                  </a>
        """
    class Meta:
        verbose_name = _("Scenario")
        verbose_name_plural = _("Scenarios")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":scenario", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f'{CoreSettings.ADMIN_URL}{APP_NAME}/scenario/{self.pk}/change/'
