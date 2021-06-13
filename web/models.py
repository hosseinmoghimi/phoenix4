from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
IMAGE_FOLDER=APP_NAME+"/img/"
from core.models import BasicPage
from django.shortcuts import reverse
class WebPage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(WebPage,self).save(*args, **kwargs)


class ResumeCategory(WebPage):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    

    class Meta:
        verbose_name = _("ResumeCategory")
        verbose_name_plural = _("ResumeCategorys")

    def save(self,*args, **kwargs):
        self.class_name="resumecategory"
        return super(ResumeCategory,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ResumeCategory_detail", kwargs={"pk": self.pk})

class Resume(WebPage):
    category=models.ForeignKey("resumecategory", verbose_name=_("category"), on_delete=models.CASCADE)

    

    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")


    def save(self,*args, **kwargs):
        self.class_name="resume"
        return super(Resume,self).save(*args, **kwargs)


class Blog(WebPage):

    

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")


    def save(self,*args, **kwargs):
        self.class_name="blog"
        return super(Blog,self).save(*args, **kwargs)

