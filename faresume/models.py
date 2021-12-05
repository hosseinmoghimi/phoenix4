from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.models import BasicPage
from faresume.apps import APP_NAME


class ResumeCategory(models.Model):
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    class_name="resumecategory"
    class Meta:
        verbose_name = _("ResumeCategory")
        verbose_name_plural = _("ResumeCategories")

    def __str__(self):
        return f"{self.title} @ {self.profile.name}"

    def get_absolute_url(self):
        return reverse(f"{APP_NAME}:{self.class_name}", kwargs={"pk": self.pk})


class Resume(BasicPage):
    category = models.ForeignKey("resumecategory", verbose_name=_(
        "category"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        self.class_name = "resume"
        return super(Resume, self).save(*args, **kwargs)
