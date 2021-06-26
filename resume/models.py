from resume.enums import FilterEnum, IconEnum
from django.db.models.fields import DateField
from core.enums import ColorEnum
from tinymce.models import HTMLField
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
IMAGE_FOLDER=APP_NAME+"/img/"
from core.models import BasicPage
from django.shortcuts import reverse



class ResumePage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(ResumePage,self).save(*args, **kwargs)




class ResumeCategory(ResumePage):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    

    class Meta:
        verbose_name = _("ResumeCategory")
        verbose_name_plural = _("ResumeCategorys")

    def save(self,*args, **kwargs):
        self.class_name="resumecategory"
        return super(ResumeCategory,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("ResumeCategory_detail", kwargs={"pk": self.pk})

class Resume(ResumePage):
    category=models.ForeignKey("resumecategory", verbose_name=_("category"), on_delete=models.CASCADE)
    start_date=models.DateField(_("start_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    end_date=models.DateField(_("end_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    location=models.CharField(_("location"),null=True,blank=True, max_length=50)

    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")


    def save(self,*args, **kwargs):
        self.class_name="resume"
        return super(Resume,self).save(*args, **kwargs)

class ResumeIndex(models.Model):
    class_name="resumeindex"
    image_header_origin =models.ImageField(_("تصویر سربرگ"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Resume/Header/', height_field=None, width_field=None, max_length=None)                              
  
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    title=models.CharField(_("title"),null=True,blank=True, max_length=100)
    typing_text=models.CharField(_("typing_text"), null=True,blank=True,default="Developer,Designer,Programmer",max_length=500)
    about_top=models.TextField(_("about_top"),null=True,blank=True)
    image_main_origin = models.ImageField(_("تصویر اصلی"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Resume/Main/', height_field=None, width_field=None, max_length=None)
    job_title=models.CharField(_("job_title"),null=True,blank=True, max_length=300)
    about_middle=models.TextField(_("about_middle"),null=True,blank=True)

    birth_day=models.DateField(_("birth_day"),null=True,blank=True, auto_now=False, auto_now_add=False)
    website=models.CharField(_("website"),null=True,blank=True, max_length=500)
    phone=models.CharField(_("phone"),null=True,blank=True, max_length=50)
    city=models.CharField(_("city"),null=True,blank=True, max_length=50)
    age=models.IntegerField(_("age"),null=True,blank=True, default=30)
    degree=models.CharField(_("degree"),null=True,blank=True, max_length=100)
    email=models.CharField(_("email"),null=True,blank=True, max_length=100)
    freelance=models.CharField(_("freelance"),null=True,blank=True, max_length=100)
    
    about_bottom=models.TextField(_("about_bottom"),null=True,blank=True)



    facts_top=models.TextField(_("facts_top"),null=True,blank=True)
    skills_top=models.TextField(_("skills_top"),null=True,blank=True)
    resume_top=models.TextField(_("resume_top"),null=True,blank=True)
    portfolio_top=models.TextField(_("portfolio_top"),null=True,blank=True)
    services_top=models.TextField(_("services_top"),null=True,blank=True)

    class Meta:
        verbose_name = _("ResumeIndex")
        verbose_name_plural = _("ResumeIndexs")

    def __str__(self):
        return (self.profile.name if self.title is None else self.title)
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)
        else:
            from .views import TEMPLATE_ROOT
            return f'{STATIC_URL}{TEMPLATE_ROOT}/img/profile-img.jpg'
    def image_header(self):
        if self.image_header_origin:
            return MEDIA_URL+str(self.image_header_origin)
        else:
            from .views import TEMPLATE_ROOT
            return f'{STATIC_URL}{TEMPLATE_ROOT}/img/hero-bg.jpg'
    
    def get_absolute_url(self):
        return reverse(APP_NAME+":resume_index", kwargs={"profile_id": self.profile.pk})
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

class ResumeService(ResumePage):

    

    class Meta:
        verbose_name = _("ResumeService")
        verbose_name_plural = _("ResumeServices")

    def save(self,*args, **kwargs):
        self.class_name="resumeservice"
        return super(ResumeService,self).save(*args, **kwargs)

class ResumePortfolio(ResumePage):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    filter=models.CharField(_("filter"),choices=FilterEnum.choices,default=FilterEnum.web, max_length=50)
    # image_main_origin =models.ImageField(_("تصویر سربرگ"), upload_to=IMAGE_FOLDER +
    #                                  'Resume/Portfolio/', height_field=None, width_field=None, max_length=None)                              
    category=models.CharField(_("category"), max_length=500)
    # priority=models.IntegerField(_("priority"),default=100)
    # def image(self):
    #     if self.image_main_origin:
    #         return MEDIA_URL+str(self.image_main_origin)
    

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

    def save(self,*args, **kwargs):
        self.class_name="resumeportfolio"
        return super(ResumePortfolio,self).save(*args, **kwargs)



class ResumeSkill(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    percentage=models.IntegerField(_("percentage"),default=10)
    class_name="resumeskill"
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


    class Meta:
        verbose_name = _("ResumeSkill")
        verbose_name_plural = _("ResumeSkills")

    def __str__(self):
        return f"""{self.profile.name} : {self.title} : {self.percentage}"""

    def get_absolute_url(self):
        return reverse("ResumeSkill_detail", kwargs={"pk": self.pk})

class ResumeFact(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=500)
    color=models.CharField(_("color"), max_length=50)
    icon=models.CharField(_("icon"),choices=IconEnum.choices, max_length=100)
    count=models.IntegerField(_("count"),default=10)
    class_name="resumefact"
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

    

    class Meta:
        verbose_name = _("ResumeFact")
        verbose_name_plural = _("ResumeFacts")

    def __str__(self):
        return f"""{self.profile.name} : {self.title} : {self.count}"""

    def get_absolute_url(self):
        return reverse("ResumeSkill_detail", kwargs={"pk": self.pk})



class ResumeTestimonial(models.Model):
    teller = models.CharField(_("teller"), max_length=2000)
    teller_description = models.CharField(_("teller_description"), max_length=2000)
    title = models.CharField(_("عنوان"), max_length=2000)
    body = models.CharField(_("متن"), max_length=2000, null=True, blank=True)
    footer = models.CharField(_("پانوشت"), max_length=200)
    priority = models.IntegerField(_("ترتیب"), default=100)
    date_added=models.DateField(_("date_added"), auto_now=False, auto_now_add=False)
    image_origin = models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Testimonial/',
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    class_name="resumetestimonial"
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_origin)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonial")

    def save(self,*args, **kwargs):
        return super(ResumeTestimonial,self).save(*args, **kwargs)



