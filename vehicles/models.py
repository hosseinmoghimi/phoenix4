from django.db.models.fields import CharField
from core.models import BasicPage
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

from core.settings import ADMIN_URL, STATIC_URL
from .apps import APP_NAME
from utility.persian import PersianCalendar
from django.utils.translation import gettext as _
from .settings import *
from .enums import *
class VehiclePage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(VehiclePage,self).save(*args, **kwargs)


class Vehicle(models.Model):
    name=models.CharField(_("نام"), max_length=50)
    vehicle_type=models.CharField(_("نوع وسیله "),choices=VehicleTypeEnum.choices,default=VehicleTypeEnum.SEDAN, max_length=50)
    brand=models.CharField(_("برند"),choices=VehicleBrandEnum.choices,default=VehicleBrandEnum.TOYOTA, max_length=50)
    model_name=models.CharField(_("مدل"),null=True,blank=True, max_length=50)
    color=models.CharField(_("رنگ"),choices=VehicleColorEnum.choices,default=VehicleColorEnum.SEFID, max_length=50)
    year=models.IntegerField(_("سال تولید"),default=2012)
    plaque=models.CharField(_("پلاک"),null=True,blank=True, max_length=50)
    owner=models.CharField(_("مالک"), max_length=50,null=True,blank=True)
    driver=models.CharField(_("راننده"), max_length=50,null=True,blank=True)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now=True, auto_now_add=False)
    kilometer=models.IntegerField(_("کیلومتر"),default=0)
    description=models.CharField(_("توضیحات"), null=True,blank=True,max_length=500)
    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def __str__(self):
        return self.brand +' ' +self.name

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/vehicle/{self.pk}/change/'

    def thumbnail(self):
        pic='trailer.jpg'
        if self.vehicle_type==VehicleTypeEnum.TRAILER:
            pic='trailer.jpg'
        if self.vehicle_type==VehicleTypeEnum.TRUCK:
            pic='truck.jpg'
        if self.vehicle_type==VehicleTypeEnum.TAXI:
            pic='taxi.jpg'
        if self.vehicle_type==VehicleTypeEnum.LOADER:
            pic='loader.jpg'
        if self.vehicle_type==VehicleTypeEnum.SEDAN:
            pic='sedan.jpg'
        if self.vehicle_type==VehicleTypeEnum.BUS:
            pic='bus.jpg'
        if self.vehicle_type==VehicleTypeEnum.GRADER:
            pic='grader.jpg'
        return f'{STATIC_URL}{APP_NAME}/images/thumbnail/{pic}/'
    def get_absolute_url(self):
        return reverse(APP_NAME+":vehicle", kwargs={"vehicle_id": self.pk})


class VehicleLocation(models.Model):
    vehicle=models.ForeignKey("vehicle", verbose_name=_("ماشین"), on_delete=models.CASCADE)
    location=models.ForeignKey("map.location", verbose_name=_("location"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)


    class Meta:
        verbose_name = _("VehicleLocation")
        verbose_name_plural = _("VehicleLocations")

    def __str__(self):
        return f'{self.vehicle.name} @ {self.location.title}'

    def get_absolute_url(self):
        return reverse("VehicleLocation_detail", kwargs={"pk": self.pk})


class Area(models.Model):
    code=models.CharField(_("code"), max_length=50)
    name=models.CharField(_("area"), max_length=50)
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/area/{self.pk}/change/'

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":area", kwargs={"area_id": self.pk})


class Driver(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    medical_license_photo=models.ForeignKey("core.image",related_name="medical_license_photoes", verbose_name=_("تصویر کارت بهداشت"),null=True,blank=True, on_delete=models.CASCADE)
    driving_license_photo=models.ForeignKey("core.image",related_name="driving_license_photoes",  verbose_name=_("تصویر گواهینامه"),null=True,blank=True, on_delete=models.CASCADE)
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":driver", kwargs={"driver_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/driver/{self.pk}/change/'


class WorkShift(models.Model):
    area=models.ForeignKey("area", verbose_name=_("area"), on_delete=models.CASCADE)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.CASCADE)
    driver=models.ForeignKey("driver", verbose_name=_("driver"), on_delete=models.CASCADE)
    start_time=models.DateTimeField(_("start_time"), auto_now=False, auto_now_add=False)
    end_time=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    income=models.IntegerField(_("درآمد"),default=0)
    outcome=models.IntegerField(_("هزینه"),default=0)
    description=models.CharField(_("توضیحات"), null=True,blank=True,max_length=500)
    class_name="workshift"
    def persian_start_time(self):
        return PersianCalendar().from_gregorian(self.start_time)
    def persian_end_time(self):
        return PersianCalendar().from_gregorian(self.end_time)
    class Meta:
        verbose_name = _("WorkShift")
        verbose_name_plural = _("WorkShifts")

    def __str__(self):
        return f'{self.vehicle.name} {self.start_time}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":workshift", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/workshift/{self.pk}/change/'
    def get_edit_btn(self):
        return f"""
                  <a target="_blank" href="{self.get_edit_url()}" title="ویرایش" class="btn btn-link btn-danger">
                    <i class="material-icons">
                        settings
                    </i>
                  </a>

        """


class ServiceMan(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    name=models.CharField(_("نام تعمیرگاه"),null=True,blank=True, max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/serviceman/{self.pk}/change/'

    class Meta:
        verbose_name = _("ServiceMan")
        verbose_name_plural = _("ServiceMans")

    def __str__(self):
        return self.name if self.name is not None else self.profile.name()

    def get_absolute_url(self):
        return reverse(APP_NAME+":service_man", kwargs={"service_man_id": self.pk})


class VehicleEvent(VehiclePage):
    # title=models.CharField(_("title"),blank=True, max_length=50)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("ماشین"), on_delete=models.CASCADE)
    event_datetime=models.DateTimeField(_("event_datetime"), auto_now=False, auto_now_add=False)
    kilometer=models.IntegerField(_("کارکرد"),null=True,blank=True)
    # description=models.CharField(_("توضیحات"), null=True,blank=True,max_length=500)
    # child_class=models.CharField(_("child_class"),default='vehicleworkevent', max_length=50)
    # images=models.ManyToManyField("core.galleryphoto",blank=True, verbose_name=_("images"))
    def save(self,*args, **kwargs):
        self.class_name="vehicleevent"
        return super(VehicleEvent,self).save(*args, **kwargs)
    def child_object(self):
        if self.child_class=="vehicleworkevent":
            return VehicleWorkEvent.objects.get(pk=self.pk)
        if self.child_class=="maintenance":
            return Maintenance.objects.get(pk=self.pk)
    class Meta:
        verbose_name = 'VehicleEvent'
        verbose_name_plural = 'VehicleEvents'
    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)


class Maintenance(VehicleEvent):
    maintenance_type=models.CharField(_("سرویس"),choices=MaintenanceEnum.choices, max_length=100)
    service_man=models.ForeignKey("serviceman", verbose_name=_("سرویس کار"),null=True,blank=True, on_delete=models.CASCADE)
    paid=models.IntegerField(_("هزینه به تومان"))
    def get_icon(self):
        icon="settings"
        color="primary"
        if self.maintenance_type==MaintenanceEnum.NEW_AIR_FILTER:
            icon="luggage"
            color='info'
        if self.maintenance_type==MaintenanceEnum.NEW_OIL_FILTER:
            icon="luggage"
            color='warning'
        if self.maintenance_type==MaintenanceEnum.REPAIR_GEARBOX:
            icon="build"
            color='primary'
        if self.maintenance_type==MaintenanceEnum.REPAIR_ENGINE:
            icon="build"
            color='danger'
        if self.maintenance_type==MaintenanceEnum.NEW_FUEL:
            icon="local_gas_station"
            color='danger'
        if self.maintenance_type==MaintenanceEnum.NEW_INSURANCE:
            icon="addchart"
            color='info'
        if self.maintenance_type==MaintenanceEnum.NEW_TIRE:
            icon="panorama_fish_eye"
            color='primary'
        if self.maintenance_type==MaintenanceEnum.NEW_WATER:
            icon="invert_colors"
            color='info'
        if self.maintenance_type==MaintenanceEnum.NEW_OIL:
            icon="opacity"
            color='warning'
        if self.maintenance_type==MaintenanceEnum.NEW_GLASS:
            icon="window"
            icon="info"
        if self.maintenance_type==MaintenanceEnum.WASH:
            icon="shower"
            color="primary"
        # icon_tag= f'<i class="material-icons">window</i>'
        return {'icon':icon,'color':color}
    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")
    def save(self):
        self.title=self.maintenance_type
        self.child_class="maintenance"
        return super(Maintenance,self).save()
    def __str__(self):
        return f'{self.service_man} {self.maintenance_type} {self.vehicle}'

    def get_absolute_url(self):
        # return super(Maintenance,self).get_absolute_url()
        return reverse(APP_NAME+":maintenance", kwargs={"maintenance_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/maintenance/{self.pk}/change/'


class VehicleWorkEvent(VehicleEvent):
    work_shift=models.ForeignKey("workshift", verbose_name=_("work_shift"), on_delete=models.CASCADE)
    event_type=models.CharField(_("event_type"),choices=WorkEventEnum.choices, max_length=50)
    class_name="vehicleworkevent"
    def get_icon(self):
        icon="settings"
        color="primary"
        if self.event_type==WorkEventEnum.BROKEN_GLASS:
            icon="luggage"
            color='info'
        if self.event_type==WorkEventEnum.FLAT_TIRE:
            icon="luggage"
            color='info'
        if self.event_type==WorkEventEnum.CRASH1:
            icon="luggage"
            color='info'
        if self.event_type==WorkEventEnum.CRASH2:
            icon="luggage"
            color='info'
        
        # icon_tag= f'<i class="material-icons">window</i>'
        return {'icon':icon,'color':color}
    
    def save(self):
        self.title=self.event_type
        self.child_class="vehicleworkevent"
        return super(VehicleWorkEvent,self).save()
    class Meta:
        verbose_name = _("VehicleWorkEvent")
        verbose_name_plural = _("VehicleWorkEvents")

    def __str__(self):
        return f'{self.work_shift} {self.event_type}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":vehicleworkevent", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/vehicleworkevent/{self.pk}/change/'
