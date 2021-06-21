
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db.models.fields.files import FileField
from realestate.enums import FloorEnum,KitchenTypeEnum
from django.db import models
from django.shortcuts import reverse
from .apps import APP_NAME
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
IMAGE_FOLDER=APP_NAME+"/media/"
class Property(models.Model):
    agent=models.ForeignKey("authentication.profile", verbose_name=_("مسئول فروش"),null=True,blank=True, on_delete=models.CASCADE)
    title=models.CharField(_("عنوان"), max_length=50)
    floor=models.CharField(_("طبقه"),max_length=50,choices=FloorEnum.choices,default=FloorEnum.HAMKAF)
    garage=models.IntegerField(_("تعداد گاراژ"),default=0)
    elevator=models.BooleanField(_("آسانسور دارد؟"),default=False)
    bed_rooms=models.IntegerField(_("تعداد خواب"),default=1)
    bath_rooms=models.IntegerField(_("تعداد سرویس بهداشتی"),default=1)
    kitchen_type=models.CharField(_("نوع آشپزخانه"),choices=KitchenTypeEnum.choices,default=KitchenTypeEnum.REGULAR, max_length=50)
    area=models.IntegerField(_("مساحت"))
    price=models.IntegerField(_("قیمت"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=500)
    description=HTMLField(_("توضیحات"),null=True,blank=True, max_length=5000)
    image_origin=models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"Property",null=True,blank=True, height_field=None, width_field=None, max_length=None)
    class_name='property'

    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+"realestate2/img/home.webp"

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Propertys")

    def __str__(self):
        return self.title
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse(APP_NAME+":property", kwargs={"pk": self.pk})


class PropertyMedia(models.Model):
    property=models.ForeignKey("property", verbose_name=_("ملک"), on_delete=models.CASCADE)
    file=models.FileField(_("file"), upload_to=IMAGE_FOLDER+"property", max_length=100)
    
    class_name='propertymedia'

    class Meta:
        verbose_name = _("PropertyMedia")
        verbose_name_plural = _("PropertyMedias")

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse(APP_NAME+":property_media", kwargs={"pk": self.pk})

class PropertyFeature(models.Model):
    property=models.ForeignKey("property", verbose_name=_("ملک"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    value=models.CharField(_("value"), max_length=50)
    class_name='propertyfeature'
    

    class Meta:
        verbose_name = _("PropertyFeature")
        verbose_name_plural = _("PropertyFeatures")

    def __str__(self):
        return self.property.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":property_feature", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'