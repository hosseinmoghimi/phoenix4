from django.db import models
from core.models import BasicPage as CoreBasicPage
from .apps import APP_NAME
from .enums import *
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL
from utility.persian import PersianCalendar
class Employee(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    organization_unit=models.ForeignKey("organizationunit", verbose_name=_("organizationunit"), on_delete=models.CASCADE)
    class_name="employee"
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"""{self.organization_unit.title} : {self.profile.name}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
 
class ProjectManagerPage(CoreBasicPage):   

    class Meta:
        verbose_name = _("ProjectManagerPage")
        verbose_name_plural = _("ProjectManagerPage")
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(ProjectManagerPage,self).save(*args, **kwargs)

class Project(ProjectManagerPage):
    
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    def save(self,*args, **kwargs):
        self.class_name="project"
        return super(Project,self).save(*args, **kwargs)


class Material(ProjectManagerPage):
    unit_name=models.CharField(_("unit_name"),choices=MaterialUnitNameEnum.choices,default=MaterialUnitNameEnum.ADAD, max_length=50)
    unit_price=models.IntegerField(_("unit_price"),default=0)

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")
    def save(self,*args, **kwargs):
        self.class_name="material"
        return super(Material,self).save(*args, **kwargs)


class OrganizationUnit(ProjectManagerPage):
    
    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("OrganizationUnits")
    def save(self,*args, **kwargs):
        self.class_name="organizationunit"
        return super(OrganizationUnit,self).save(*args, **kwargs)




class MaterialRequest(models.Model):
    material=models.ForeignKey("Material", verbose_name=_("متریال"), on_delete=models.PROTECT)
    quantity=models.IntegerField(_("تعداد"))
    unit_name=models.CharField(_("واحد"),max_length=50)
    unit_price=models.IntegerField(_("فی"))
    project=models.ForeignKey("Project", verbose_name=_("پروژه"), on_delete=models.CASCADE)
    description=models.CharField(_("توضیحات"),null=True,blank=True,default='', max_length=50)
    profile=models.ForeignKey("authentication.Profile", verbose_name=_("تحویل گیرنده"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("تاریخ درخواست"), auto_now=False, auto_now_add=True)
    date_delivered=models.DateTimeField(_("تاریخ درخواست"),null=True,blank=True, auto_now=False, auto_now_add=False)
    status=models.CharField(_("وضعیت"),choices=MaterialRequestStatusEnum.choices,default=MaterialRequestStatusEnum.DEFAULT, max_length=50)

    class_name='materialrequest'
    def can_be_edited(self):
        return self.project.can_be_edited
    def get_project_url(self):
        return self.project.get_absolute_url()
    def project_title(self):
        return self.project.title
    class Meta:
        verbose_name = _("درخواست متریال")
        verbose_name_plural = _("درخواست های متریال")
    def persian_date_delivered(self):
        if self.date_delivered is not None:
            return PersianCalendar().from_gregorian(self.date_delivered)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def __str__(self):
        return f'{self.project.title} ___  {self.material.title} #{self.quantity} {self.unit_name}'

    def get_absolute_url(self):
        return reverse(f'{APP_NAME}:{self.class_name}', kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""
    def signatures(self):
        return MaterialRequestSignature.objects.filter(materialrequest=self).order_by('-date_added')
    def line_total(self):
        return self.quantity*self.unit_price
    def save(self,*args, **kwargs):
        # updated=False
    
        # material_order=self.project.get_material_order
        # if material_order is not None:
        #     for line in material_order.orderline_set.all():
        #         if line.product==self.material.product:
        #             line.quantity=self.quantity
        #             line.unit_price=self.unit_price
        #             line.unit_name=self.unit_name
        #             line.save()
        #             updated=True
        #     if not updated:
        #         line=OrderLine(product=self.material.product,unit_name=self.unit_name,quantity=self.quantity,unit_price=self.unit_price,order=material_order)
        #         line.save()
        return super(MaterialRequest,self).save(*args, **kwargs)

class MaterialRequestSignature(models.Model):
    materialrequest=models.ForeignKey("materialrequest", verbose_name=_("درخواست"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.Profile", verbose_name=_("profile"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("description"), max_length=200)
    status=models.CharField(_("status"),choices=SignatureStatusEnum.choices,default=SignatureStatusEnum.DEFAULT, max_length=200)
    class Meta:
        verbose_name = _("امضای درخواست متریال")
        verbose_name_plural = _("امضا های درخواست متریال")

    def __str__(self):
        return f'{self.profile.name()} : {self.description} @ {PersianCalendar().from_gregorian(self.date_added)}'

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    
    def get_status_color(self):
      return StatusColor(self.status)