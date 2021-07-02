
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db.models.fields.files import FileField
from realestate.enums import CarBrandEnum, FloorEnum,KitchenTypeEnum
from django.db import models
from django.shortcuts import reverse
from .apps import APP_NAME
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
from accounting.models import Asset
IMAGE_FOLDER=APP_NAME+"/media/"


class Property(Asset):
    agent=models.ForeignKey("authentication.profile", verbose_name=_("مسئول فروش"),null=True,blank=True, on_delete=models.CASCADE)
    floor=models.CharField(_("طبقه"),max_length=50,choices=FloorEnum.choices,default=FloorEnum.HAMKAF)
    garage=models.IntegerField(_("تعداد گاراژ"),default=0)
    elevator=models.BooleanField(_("آسانسور دارد؟"),default=False)
    bed_rooms=models.IntegerField(_("تعداد خواب"),default=1)
    bath_rooms=models.IntegerField(_("تعداد سرویس بهداشتی"),default=1)
    kitchen_type=models.CharField(_("نوع آشپزخانه"),choices=KitchenTypeEnum.choices,default=KitchenTypeEnum.REGULAR, max_length=50)
    area=models.IntegerField(_("مساحت"))
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=500)
    class_name='property'
    location=models.CharField(_("location"),null=True,blank=True, max_length=5000)
    
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+"realestate2/img/home.webp"

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Propertys")
    def save(self,*args, **kwargs):
        if self.location is not None:
            self.location=self.location.replace('width="600"','width="100%"')
            self.location=self.location.replace('height="450"','height="700"')
        return super(Property,self).save(*args, **kwargs)

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse(APP_NAME+":property", kwargs={"pk": self.pk})

class Car(Asset):
    brand=models.CharField(_("brand"),choices=CarBrandEnum.choices, max_length=50)
    product=models.CharField(_("محصول"), max_length=50)
    color=models.CharField(_("رنگ"), max_length=50)
    distance=models.IntegerField(_("کارکرد به کیلومتر"))


    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+"realestate2/img/car.webp"
    

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")


    def get_absolute_url(self):
        return reverse(APP_NAME+":car", kwargs={"car_id": self.pk})


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