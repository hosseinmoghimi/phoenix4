from django.db import models
from core.models import BasicPage as CoreBasicPage
from .apps import APP_NAME
from .enums import *
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from utility.persian import PersianCalendar
IMAGE_FOLDER=APP_NAME+"/images/"


class Employer(models.Model):
    pre_title=models.CharField(_("pre_title"), null=True,blank=True,max_length=50)
    title=models.CharField(_("title"), max_length=50)
    image_origin=models.ImageField(_("image"), null=True,blank=True,upload_to=IMAGE_FOLDER+"employer/image/", height_field=None, width_field=None, max_length=None)
    logo_origin=models.ImageField(_("logo"), null=True,blank=True,upload_to=IMAGE_FOLDER+"employer/logo/", height_field=None, width_field=None, max_length=None)
    owner=models.ForeignKey("authentication.Profile",null=True,blank=True, verbose_name=_("owner"), on_delete=models.CASCADE)
    def logo(self):
        if self.logo_origin:
            return f"{MEDIA_URL}{self.logo_origin}"
        return f"{STATIC_URL}{APP_NAME}/img/pages/thumbnail/employer-logo.png"
    def image(self):
        if self.image_origin:
            return f"{MEDIA_URL}{self.image_origin}"
        return f"{STATIC_URL}{APP_NAME}/img/pages/thumbnail/employer.jpg"
    class Meta:
        verbose_name = _("Employer")
        verbose_name_plural = _("Employers")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+":employer", kwargs={"pk": self.pk})
     
    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/employer/{self.pk}/change/"""


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
    def get_edit_btn(self):
        return f"""
        <a  target="_blank" title="ویرایش {self.title}" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """


class ProjectManagerPage(CoreBasicPage):
    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""
    
    class Meta:
        verbose_name = _("ProjectManagerPage")
        verbose_name_plural = _("ProjectManagerPage")
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(ProjectManagerPage,self).save(*args, **kwargs)
  
class Project(ProjectManagerPage):
    percentage_completed=models.IntegerField(_("درصد تکمیل پروژه"),default=0)
    start_date=models.DateTimeField(_("زمان شروع پروژه"),null=True,blank=True, auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("زمان پایان پروژه"),null=True,blank=True, auto_now=False, auto_now_add=False)
    organization_units=models.ManyToManyField("OrganizationUnit", verbose_name=_("واحد های سازمانی"),blank=True)
    employer=models.ForeignKey("employer",null=True,blank=True, related_name="projects_out",verbose_name=_("کارفرما"), on_delete=models.CASCADE)
    contractor=models.ForeignKey("employer",null=True,blank=True, related_name="projects_in",verbose_name=_("پیمانکار"), on_delete=models.CASCADE)
    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)
    def get_services_order_url(self):
        return reverse(APP_NAME+':project_services_order',kwargs={'pk':self.pk})
    def get_materials_order_url(self):
        return reverse(APP_NAME+':project_materials_order',kwargs={'pk':self.pk})
    def get_chart_url(self):
        return reverse(APP_NAME+':projects_chart',kwargs={'pk':self.pk})
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    def parent_project(self):
        return Project.objects.filter(pk=self.parent_id).first()
    def save(self,*args, **kwargs):


        self.class_name="project"
        if self.contractor is None and self.parent is not None:
            self.contractor=self.parent_project().contractor
        if self.employer is None and self.parent is not None:
            self.employer=self.parent_project().employer
        return super(Project,self).save(*args, **kwargs)
    def sum_material_requests(self):
        sum=0
        for material_request in self.materialrequest_set.all():
            sum+=material_request.quantity*material_request.unit_price
        return sum
    def sum_total(self):
        sum= self.sum_material_requests()+self.sum_service_requests()
        for proj in self.sub_projects():
            sum+=proj.sum_total()
        return sum
    def sum_service_requests(self):
        sum=0
        for service_request in self.servicerequest_set.all():
            sum+=service_request.quantity*service_request.unit_price
        return sum
    def sub_projects(self):
        return Project.objects.filter(parent_id=self.id).order_by('priority')
    def employees(self):
        employees=[]
        for org in self.organization_units.all():
            for emp in org.employee_set.all():
                employees.append(emp.id)
        return Employee.objects.filter(id__in=employees)
class Material(ProjectManagerPage):
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    unit_price=models.IntegerField(_("unit_price"),default=0)
    def childs(self):
        return Material.objects.filter(parent=self)
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")
    def save(self,*args, **kwargs):
        self.class_name="material"
        return super(Material,self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image_thumbnail_origin:
            return super(Material,self).thumbnail()
        return STATIC_URL+"projectmanager/img/pages/thumbnail/material.png"


class Service(ProjectManagerPage):
    # service_date=models.DateTimeField(_("تاریخ ارائه خدمات"), auto_now=False, auto_now_add=False)
    # project_for=models.ForeignKey("Project",related_name='workservices', verbose_name=_("پروژه مرتبط"), on_delete=models.CASCADE)
    unit_price=models.IntegerField(_("هزینه پیش فرض خدمات"))
    unit_name=models.CharField(_("نام واحد"),max_length=50)
    def childs(self):
        return Service.objects.filter(parent_id=self.pk)
    def save(self,*args, **kwargs):
        self.class_name='service'
        super(Service,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("خدمات")
        verbose_name_plural = _("خدمات")
    
class Event(ProjectManagerPage):
    project_related=models.ForeignKey("project", verbose_name=_("project"), on_delete=models.CASCADE)
    event_datetime=models.DateTimeField(_("event_datetime"), auto_now=False, auto_now_add=False)
    adder=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    def save(self,*args, **kwargs):
        self.class_name="event"
        return super(Event,self).save(*args, **kwargs)

    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)
    class Meta:
        verbose_name = _("رویداد")
        verbose_name_plural = _("رویداد ها")
    


class ProjectLocation(models.Model):
    title=models.CharField(_("عنوان نقطه"),max_length=50,null=True,blank=True)
    location=models.CharField(_("لوکیشن"),max_length=1000)
    project=models.ForeignKey("Project", verbose_name=_("پروژه"), on_delete=models.CASCADE)
    class_name="projectlocation"
    class Meta:
        verbose_name = _("موقعیت پروژه")
        verbose_name_plural = _("موقعیت های پروژه ها")
    def __str__(self):
        return f'{self.project} {self.project.title} {self.title}'
    def project_title(self):
        return self.project.title
    def get_project_url(self):
        return self.project.get_absolute_url()
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def save(self,*args, **kwargs):
        self.location=self.location.replace('width="600"','width="100%"')
        self.location=self.location.replace('height="450"','height="400"')
        super(ProjectLocation,self).save(*args, **kwargs)


class OrganizationUnit(ProjectManagerPage):
    employer=models.ForeignKey("employer", verbose_name=_("employer"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("OrganizationUnits")
    def save(self,*args, **kwargs):
        self.class_name="organizationunit"
        return super(OrganizationUnit,self).save(*args, **kwargs)
    def employees(self):
        return self.employee_set.all()
    @property
    def full_title(self):
        if self.parent is None:
            return self.title
        return self.title+" " +OrganizationUnit.objects.get(pk=self.parent.id).full_title
    def childs(self):
        return OrganizationUnit.objects.filter(parent_id=self.id)
class EmployeeSpeciality(ProjectManagerPage):
    employee=models.ForeignKey("employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    max=models.IntegerField(_("max"))
    value=models.IntegerField(_("value"))
    percent=models.IntegerField(_("percent"))
    verified=models.BooleanField(_("verified"),default=False)
    class Meta:
        verbose_name = _("EmployeeSpeciality")
        verbose_name_plural = _("EmployeeSpecialitys")

    def __str__(self):
        return f"""{self.employee} {self.title}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":employee_speciality", kwargs={"pk": self.pk})



class MaterialRequest(models.Model):
    material=models.ForeignKey("Material", verbose_name=_("متریال"), on_delete=models.PROTECT)
    quantity=models.IntegerField(_("تعداد"))
    unit_name=models.CharField(_("واحد"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD,max_length=50)
    unit_price=models.IntegerField(_("فی"))
    project=models.ForeignKey("Project", verbose_name=_("پروژه"), on_delete=models.CASCADE)
    description=models.CharField(_("توضیحات"),null=True,blank=True,default='', max_length=50)
    profile=models.ForeignKey("authentication.Profile", verbose_name=_("تحویل گیرنده"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("تاریخ درخواست"), auto_now=False, auto_now_add=True)
    date_delivered=models.DateTimeField(_("تاریخ درخواست"),null=True,blank=True, auto_now=False, auto_now_add=False)
    status=models.CharField(_("وضعیت"),choices=RequestStatusEnum.choices,default=RequestStatusEnum.REQUESTED, max_length=50)

    class_name='materialrequest'
    def can_be_edited(self):
        return self.project.can_be_edited
    
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
    def get_edit_btn(self):
        return f"""
        <a  target="_blank" title="ویرایش" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """
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


class ServiceRequest(models.Model):
    project=models.ForeignKey("Project", verbose_name=_("پروژه"), on_delete=models.CASCADE)
    service=models.ForeignKey("service", verbose_name=_("service"), on_delete=models.PROTECT)
    quantity=models.IntegerField(_("تعداد"))
    unit_name=models.CharField(_("واحد"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD,max_length=50)
    unit_price=models.IntegerField(_("فی"))
    description=models.CharField(_("توضیحات"),null=True,blank=True,default='', max_length=50)
    profile=models.ForeignKey("authentication.Profile", verbose_name=_("تحویل گیرنده"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("تاریخ درخواست"), auto_now=False, auto_now_add=True)
    date_delivered=models.DateTimeField(_("تاریخ درخواست"),null=True,blank=True, auto_now=False, auto_now_add=False)
    status=models.CharField(_("وضعیت"),choices=RequestStatusEnum.choices,default=RequestStatusEnum.REQUESTED, max_length=50)
    employee=models.ForeignKey("employee",null=True,blank=True, verbose_name=_("employee"), on_delete=models.CASCADE)
    class_name='servicerequest'
    def can_be_edited(self):
        return self.project.can_be_edited
    
    class Meta:
        verbose_name = _("درخواست سرویس")
        verbose_name_plural = _("درخواست های سرویس")
    def persian_date_delivered(self):
        if self.date_delivered is not None:
            return PersianCalendar().from_gregorian(self.date_delivered)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def __str__(self):
        return f'{self.project.title} ___  {self.service.title} #{self.quantity} {self.unit_name}'

    def get_absolute_url(self):
        return reverse(f'{APP_NAME}:{self.class_name}', kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'
    def get_edit_btn(self):
        return f"""
        <a  target="_blank" title="ویرایش" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """
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
        return super(ServiceRequest,self).save(*args, **kwargs)


class ServiceRequestSignature(models.Model):
    service_request=models.ForeignKey("servicerequest", verbose_name=_("درخواست"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.Profile", verbose_name=_("profile"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("description"), max_length=200)
    status=models.CharField(_("status"),choices=SignatureStatusEnum.choices,default=SignatureStatusEnum.REQUESTED, max_length=200)
    class Meta:
        verbose_name = _("امضای درخواست سرویس")
        verbose_name_plural = _("امضا های درخواست سرویس")

    def __str__(self):
        return f'{self.profile.name} : {self.description} @ {PersianCalendar().from_gregorian(self.date_added)}'

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    
    def get_status_color(self):
      return StatusColor(self.status)

    def get_status_tag(self):
        return f"""
            <span class="badge badge-{self.get_status_color()}">{self.status}</span>
        """

   
   
    def get_edit_btn(self):
        return f"""
            <a target="_blank" title="ویرایش" href="{self.get_edit_url()}">
               <i class="material-icons">
                    edit
                </i>
            </a>
        """

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/servicerequestsignature/{self.pk}/change/"

class MaterialRequestSignature(models.Model):
    material_request=models.ForeignKey("materialrequest", verbose_name=_("درخواست"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.Profile", verbose_name=_("profile"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("description"), max_length=200)
    status=models.CharField(_("status"),choices=SignatureStatusEnum.choices,default=SignatureStatusEnum.REQUESTED, max_length=200)
    class Meta:
        verbose_name = _("امضای درخواست متریال")
        verbose_name_plural = _("امضا های درخواست متریال")

    def __str__(self):
        return f'{self.profile.name} : {self.description} @ {PersianCalendar().from_gregorian(self.date_added)}'

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    
    def get_status_color(self):
      return StatusColor(self.status)
    
    def get_status_tag(self):
        return f"""
            <span class="badge badge-{self.get_status_color()}">{self.status}</span>
        """

    def get_edit_btn(self):
        return f"""
            <a target="_blank" title="ویرایش" href="{self.get_edit_url()}">
               <i class="material-icons">
                    edit
                </i>
            </a>
        """

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/materialrequestsignature/{self.pk}/change/"
