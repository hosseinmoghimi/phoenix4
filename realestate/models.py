
from core.settings import ADMIN_URL
from django.db.models.fields.files import FileField
from realestate.enums import FloorEnum,KitchenTypeEnum
from django.db import models
from django.shortcuts import reverse
from .apps import APP_NAME
from django.utils.translation import gettext as _
IMAGE_FOLDER=APP_NAME+"/media/"
class Property(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    floor=models.CharField(_("طبقه"),max_length=50,choices=FloorEnum.choices,default=FloorEnum.HAMKAF)
    parking=models.IntegerField(_("تعداد پارکینگ"),default=0)
    elevator=models.BooleanField(_("آسانسور دارد؟"),default=False)
    bed_rooms=models.IntegerField(_("تعداد خواب"),default=1)
    bath_rooms=models.IntegerField(_("تعداد سرویس بهداشتی"),default=1)
    kitchen_type=models.CharField(_("نوع آشپزخانه"),choices=KitchenTypeEnum.choices,default=KitchenTypeEnum.REGULAR, max_length=50)
    area=models.IntegerField(_("مساحت"))
    price=models.IntegerField(_("قیمت"))
    description=models.CharField(_("توضیحات"),null=True,blank=True, max_length=500)
    class_name='property'

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
    

    class Meta:
        verbose_name = _("PropertyMedia")
        verbose_name_plural = _("PropertyMedias")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":property_media", kwargs={"pk": self.pk})
