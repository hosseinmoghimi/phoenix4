from tinymce.models import HTMLField
from core.settings import ADMIN_URL, MEDIA_URL
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

class Carousel(models.Model):
    app_name=models.CharField(_("app_name"), max_length=50)
    image_banner = models.ImageField(_("تصویر اسلایدر  1333*2000 "), upload_to=IMAGE_FOLDER +
                                     'Banner/', height_field=None, width_field=None, max_length=None)
    title = models.CharField(_("عنوان"), null=True, blank=True, max_length=500)
    body = HTMLField(_("بدنه"), null=True, blank=True, max_length=2000)
    text_color = models.CharField(_("رنگ متن"), default="#fff", max_length=20)

    priority = models.IntegerField(_("ترتیب"), default=100)
    archive = models.BooleanField(_("بایگانی شود؟"), default=False)
    tag_number = models.IntegerField(_("عدد برچسب"), default=100)
    tag_text = models.CharField(
        _("متن برچسب"), max_length=100, blank=True, null=True)
    class_name="carousel"
    class Meta:
        verbose_name = _("Carousel")
        verbose_name_plural = _("اسلایدر های صفحه اصلی")

    def image(self):
        return MEDIA_URL+str(self.image_banner)

    def __str__(self):
        return str(self.priority)

    def get_edit_btn(self):
        return f"""
        <a target="_blank" href="{self.get_edit_url()}" title="ویرایش اسلایدر">
        <i class="fa fa-edit text-info"></i>
        </a>
        """
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'