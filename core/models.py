from django.db import models
from django.db.models.fields import BooleanField
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .settings import *
from django.shortcuts import reverse
from .enums import *

IMAGE_FOLDER = APP_NAME+'/images/'

class Icon(models.Model):
    name=models.CharField(_("name"), null=True,blank=True,max_length=50)
    icon_fa=models.CharField(_("fa"), null=True,blank=True,max_length=50)
    icon_material=models.CharField(_("material_icon"),null=True,blank=True, max_length=50)
    icon_svg=models.CharField(_("svg_icon"),null=True,blank=True, max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    width = models.IntegerField(_("عرض آیکون"), null=True, blank=True)
    height = models.IntegerField(_("ارتفاع آیکون"), null=True, blank=True)
    image_origin = models.ImageField(_("تصویر آیکون"), upload_to=IMAGE_FOLDER+'Icon/',
                                     height_field=None, null=True, blank=True, width_field=None, max_length=None)
    
    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")

    def __str__(self):
        return self.name

    def get_icon_tag(self, icon_style='', color=None,no_color=False):
        
        if color is not None:
            self.color = color
        text_color=''
        if not no_color and self.color is not None:
            text_color='text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''


class Tag(models.Model):
    priority = models.IntegerField(_("ترتیب"), default=100)
    title = models.CharField(_("عنوان"), max_length=50)
    icon=models.ForeignKey("Icon", verbose_name=_("icon"),null=True,blank=True, on_delete=models.CASCADE)
    


class Image(models.Model):
    title = models.CharField(
        _("عنوان تصویر"), max_length=100, null=True, blank=True)
    description = models.CharField(
        _("شرح تصویر"), max_length=500, null=True, blank=True)
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Gallery/Photo/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)
    image_main_origin = models.ImageField(_("تصویر اصلی"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Gallery/Photo/Main/', height_field=None, width_field=None, max_length=None)
    image_header_origin =models.ImageField(_("تصویر سربرگ"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Gallery/Photo/Header/', height_field=None, width_field=None, max_length=None)                              
   
    archive = models.BooleanField(_("بایگانی شود?"), default=False)
    priority = models.IntegerField(_("ترتیب"), default=100)
    location = models.CharField(
        _("موقعیت مکانی تصویر"), max_length=50, null=True, blank=True)
    profile = models.ForeignKey("authentication.profile", null=True,
                                blank=True, verbose_name=_("پروفایل"), on_delete=models.SET_NULL)

    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    

    class Meta:
        verbose_name = _("GalleryPhoto")
        verbose_name_plural = _("تصاویر")

    

    def get_absolute_url(self):
        return MEDIA_URL+str(self.image_main_origin)

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/galleryphoto/{self.pk}/change/'

class BasicPage(models.Model):
    for_home=models.BooleanField(_("for_home"),default=False)
    parent = models.ForeignKey("basicpage",related_name="childs", verbose_name=_(
        "basicpage"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    icon = models.ForeignKey("icon", verbose_name=_(
        "icon"), null=True, blank=True, on_delete=models.CASCADE)
    panel = models.CharField(_("panel"), null=True, blank=True, max_length=50)
    short_description = models.CharField(
        _("short_description"), null=True, blank=True, max_length=50)
    description = models.CharField(
        _("description"), null=True, blank=True, max_length=50)
    image_thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Page/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)
    image_header_origin =models.ImageField(_("تصویر سربرگ"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Page/Header/', height_field=None, width_field=None, max_length=None)                              
    image_main_origin = models.ImageField(_("تصویر اصلی"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Page/Main/', height_field=None, width_field=None, max_length=None)
    
    archive = models.BooleanField(_("بایگانی شود؟"), default=False)
    
    priority = models.IntegerField(_('ترتیب'), default=100)

    creator = models.ForeignKey("authentication.profile", verbose_name=_(
        "creator"), null=True, blank=True, on_delete=models.SET_NULL)


    color = models.CharField(_("color"), blank=True, null=True,
                             choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)
    tags = models.ManyToManyField(
        "Tag", verbose_name=_("برچسب ها"), blank=True)
    meta_data=models.CharField(_("MetaData"), max_length=100)
    app_name = models.CharField(_("app_name"), max_length=50)
    class_name = models.CharField(_("class_name"), max_length=50)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    
    class Meta:
        verbose_name = _("BasicPage")
        verbose_name_plural = _("BasicPages")

    def __str__(self):
        try:
            return f"{self.app_name}:{self.class_name}  {self.title}"
        except:
            return "sdssdsdsdsdsd"

    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
    def get_edit_btn(self):
        return f"""
        <a title="ویرایش {self.title}" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """
    def get_absolute_url(self):
        return reverse(self.app_name+":"+self.class_name, kwargs={"pk": self.pk})



class Parameter(models.Model):
    app_name=models.CharField(_("app_name"),choices=AppNameEnum.choices,null=True,blank=True,max_length=20)
    name = models.CharField(_("نام"), max_length=50)
    value_origin = models.CharField(_("مقدار"),null=True,blank=True, max_length=10000)
    def value(self):
        if self.value_origin is None:
            return ''
        return self.value_origin
    def get_edit_btn(self):
        return f"""
         <a target="_blank" title="ویرایش {self.name}" class="btn btn-info btn-link" href="{self.get_edit_url()}">
                            <i class="material-icons"   aria-hidden="true" >settings</i>
                        </a>
        """

    class Meta:
        verbose_name = _("پارامتر")
        verbose_name_plural = _("پارامتر ها")

    def __str__(self):
        return f'{self.app_name} :{self.name} : {self.value_origin}'

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/change/'

    def save(self):
        if self.name==ParametersEnum.LOCATION:
            self.value_origin=self.value_origin.replace('width="600"','width="100%"')
            self.value_origin=self.value_origin.replace('height="450"','height="400"') 
        super(Parameter,self).save()
