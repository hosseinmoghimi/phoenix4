from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .enums import *
from django.shortcuts import reverse

class Game(models.Model):
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    scenario=models.CharField(_("scenario"),choices=GameScenarioEnum.choices,max_length=50)
    god=models.ForeignKey("player", verbose_name=_(""), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":game", kwargs={"pk": self.pk})

class Player(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    score=models.IntegerField(_("score"),default=0)
    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")

    def __str__(self):
        return self.name
    @property
    def bio(self):
        return self.profile.bio if self.profile.bio is not None else ""
    @property
    def name(self):
        return self.profile.name
    @property
    def image(self):
        return self.profile.image
    def get_absolute_url(self):
        return reverse(APP_NAME+":player", kwargs={"pk": self.pk})

class God(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    score=models.IntegerField(_("score"),default=0)
    class Meta:
        verbose_name = _("God")
        verbose_name_plural = _("Gods")

    def __str__(self):
        return self.name
    @property
    def name(self):
        return self.profile.name
    @property
    def image(self):
        return self.profile.image
    def get_absolute_url(self):
        return reverse(APP_NAME+":god", kwargs={"pk": self.pk})
