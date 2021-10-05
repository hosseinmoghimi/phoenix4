from django.db import models
from django.db.models.fields import CharField
from core.models import BasicPage as CoreBasicPage
from .apps import APP_NAME
from .enums import *
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from utility.persian import PersianCalendar
IMAGE_FOLDER = APP_NAME+"/images/"


class ProjectManagerPage(CoreBasicPage):
    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""

    class Meta:
        verbose_name = _("ProjectManagerPage")
        verbose_name_plural = _("ProjectManagerPage")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(ProjectManagerPage, self).save(*args, **kwargs)


class Employer(models.Model):
    pre_title = models.CharField(
        _("pre_title"), null=True, blank=True, max_length=50)
    title = models.CharField(_("title"), max_length=50)
    image_origin = models.ImageField(_("image"), null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     "employer/image/", height_field=None, width_field=None, max_length=None)
    logo_origin = models.ImageField(_("logo"), null=True, blank=True, upload_to=IMAGE_FOLDER +
                                    "employer/logo/", height_field=None, width_field=None, max_length=None)
    owner = models.ForeignKey("authentication.Profile", null=True,
                              blank=True, verbose_name=_("owner"), on_delete=models.CASCADE)
    home_page = models.CharField(
        _("home page"), null=True, blank=True, max_length=100)
    address = models.CharField(
        _("Address"), null=True, blank=True, max_length=200)
    postal_code = models.CharField(
        _("postal_code"), null=True, blank=True, max_length=50)
    email = models.CharField(_("email"), null=True, blank=True, max_length=80)
    tel = models.CharField(_("tel"), null=True, blank=True, max_length=50)
    fax = models.CharField(_("fax"), null=True, blank=True, max_length=50)
    description = models.TextField(_("description"), null=True, blank=True)

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

    def get_edit_btn(self):
        return f"""
        <a  target="_blank" title="ویرایش {self.title}" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """


class Employee(models.Model):
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)
    organization_unit = models.ForeignKey("organizationunit", verbose_name=_(
        "organizationunit"), on_delete=models.CASCADE)
    class_name = "employee"

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

    def get_dashboard_url(self):
        return reverse(APP_NAME+":dashboard", kwargs={'employee_id': self.pk})

    def my_projects(self):
        ids = []
        # for org in self.organization_unit_set.all():
        for proj in self.organization_unit.project_set.all():
            ids.append(proj.id)
        return Project.objects.filter(id__in=ids)



class Project(ProjectManagerPage):
    percentage_completed = models.IntegerField(
        _("درصد تکمیل پروژه"), default=0)
    start_date = models.DateTimeField(
        _("زمان شروع پروژه"), null=True, blank=True, auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(
        _("زمان پایان پروژه"), null=True, blank=True, auto_now=False, auto_now_add=False)
    organization_units = models.ManyToManyField(
        "OrganizationUnit", verbose_name=_("واحد های سازمانی"), blank=True)
    employer = models.ForeignKey("employer", null=True, blank=True, related_name="projects_out", verbose_name=_(
        "کارفرما"), on_delete=models.CASCADE)
    contractor = models.ForeignKey("employer", null=True, blank=True, related_name="projects_in", verbose_name=_(
        "پیمانکار"), on_delete=models.CASCADE)
    weight = models.IntegerField(_("ضریب و وزن پروژه"), default=10)
    locations = models.ManyToManyField(
        "location", blank=True, verbose_name=_("locations"))

    def get_event_chart_url(self):
        return reverse(APP_NAME+":project_events_chart", kwargs={'project_id': self.pk})

    def get_event_chart_url2(self):
        return reverse(APP_NAME+":project_events_chart2", kwargs={'project_id': self.pk})

    def get_event_chart_url3(self):
        return reverse(APP_NAME+":project_events_chart3", kwargs={'project_id': self.pk})
    # auto_percentage_completed=models.IntegerField(_("درصد تکمیل خودکار پروژه"),default=0)

    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)

    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)

    def get_services_order_url(self):
        return reverse(APP_NAME+':project_services_order', kwargs={'pk': self.pk})

    def get_guantt_chart_url(self):
        return reverse(APP_NAME+':guantt', kwargs={'project_id': self.pk})

    def get_materials_order_url(self):
        return reverse(APP_NAME+':project_materials_order', kwargs={'pk': self.pk})

    def auto_percentage_completed(self):
        sub_projects = self.sub_projects()
        if len(sub_projects) == 0:
            return self.percentage_completed
        auto_percentage_completed = 0
        sum_weight = 0
        for sub_project in sub_projects:
            auto_percentage_completed += sub_project.weight * \
                (sub_project.auto_percentage_completed())
            sum_weight += sub_project.weight
        auto_percentage_completed = auto_percentage_completed/sum_weight

        return round(auto_percentage_completed, 2)

    def sum_weight(self):
        sum_weight = 0
        sub_projects = self.sub_projects()
        if len(sub_projects) == 0:
            return 0
        for sub_project in sub_projects:
            sum_weight += sub_project.weight
        return sum_weight

    def get_chart_url(self):
        return reverse(APP_NAME+':projects_chart', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def parent_project(self):
        return Project.objects.filter(pk=self.parent_id).first()

    def save(self, *args, **kwargs):

        self.class_name = "project"
        if self.contractor is None and self.parent is not None:
            self.contractor = self.parent_project().contractor
        if self.employer is None and self.parent is not None:
            self.employer = self.parent_project().employer
        return super(Project, self).save(*args, **kwargs)

    def sum_material_requests(self):
        sum = 0
        for material_request in self.request_set.filter(request_type=RequestTypeEnum.MATERIAL_REQUEST):
            sum += material_request.quantity*material_request.unit_price
        return sum

    def sum_total(self):
        sum = self.sum_material_requests()+self.sum_service_requests()
        for proj in self.sub_projects():
            sum += proj.sum_total()
        return sum

    def sum_service_requests(self):
        sum = 0
        for service_request in self.request_set.filter(request_type=RequestTypeEnum.SERVICE_REQUEST):
            sum += service_request.quantity*service_request.unit_price
        return sum

    def sub_projects(self):
        return Project.objects.filter(parent_id=self.id).order_by('priority')

    def employees(self):
        employees = []
        for org in self.organization_units.all():
            for emp in org.employee_set.all():
                employees.append(emp.id)
        return Employee.objects.filter(id__in=employees)


class Material(ProjectManagerPage):
    unit_name = models.CharField(
        _("unit_name"), choices=UnitNameEnum.choices, default=UnitNameEnum.ADAD, max_length=50)
    unit_price = models.IntegerField(_("unit_price"), default=0)

    def childs(self):
        return Material.objects.filter(parent=self)

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def save(self, *args, **kwargs):
        self.class_name = "material"
        return super(Material, self).save(*args, **kwargs)

    def thumbnail(self):
        if self.image_thumbnail_origin:
            return super(Material, self).thumbnail()
        return STATIC_URL+"projectmanager/img/pages/thumbnail/material.png"

    def count_requested(self):
        count = 0
        for req in self.materialrequest_set.all():
            count += req.quantity
        return count

    def sum_price_requested(self):
        sum = 0
        for req in self.materialrequest_set.all():
            sum += (req.quantity*req.unit_price)
        return sum


class Service(ProjectManagerPage):
    # service_date=models.DateTimeField(_("تاریخ ارائه خدمات"), auto_now=False, auto_now_add=False)
    # project_for=models.ForeignKey("Project",related_name='workservices', verbose_name=_("پروژه مرتبط"), on_delete=models.CASCADE)
    unit_price = models.IntegerField(_("هزینه پیش فرض خدمات"), default=0)
    unit_name = models.CharField(_("نام واحد"), max_length=50, default="سرویس")

    def childs(self):
        return Service.objects.filter(parent_id=self.pk)

    def save(self, *args, **kwargs):
        self.class_name = 'service'
        super(Service, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("خدمات")
        verbose_name_plural = _("خدمات")


class Event(ProjectManagerPage):
    project_related = models.ForeignKey(
        "project", verbose_name=_("project"), on_delete=models.CASCADE)
    event_datetime = models.DateTimeField(
        _("event_datetime"), auto_now=False, auto_now_add=False)
    start_datetime = models.DateTimeField(
        _("start_datetime"), auto_now=False, auto_now_add=False)
    end_datetime = models.DateTimeField(
        _("end_datetime"), auto_now=False, auto_now_add=False)
    locations = models.ManyToManyField(
        "location", blank=True, verbose_name=_("locations"))
    # adder=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.class_name = "event"
        return super(Event, self).save(*args, **kwargs)

    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)

    def persian_start_datetime(self):
        return PersianCalendar().from_gregorian(self.start_datetime)

    def persian_end_datetime(self):
        return PersianCalendar().from_gregorian(self.end_datetime)

    def start_datetime2(self):
        return self.start_datetime.strftime("%Y-%m-%d %H:%M")

    def end_datetime2(self):
        return self.end_datetime.strftime("%Y-%m-%d %H:%M")

    class Meta:
        verbose_name = _("رویداد")
        verbose_name_plural = _("رویداد ها")


class Location(models.Model):
    title = models.CharField(
        _("عنوان نقطه"), max_length=50, null=True, blank=True)
    location = models.CharField(_("لوکیشن"), max_length=1000)
    creator = models.ForeignKey("authentication.profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    class_name = "location"

    class Meta:
        verbose_name = _("لوکیشن")
        verbose_name_plural = _("لوکیشن ها")

    def __str__(self):
        return f'{self.title}'

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

    def save(self, *args, **kwargs):
        self.location = self.location.replace('width="600"', 'width="100%"')
        self.location = self.location.replace('height="450"', 'height="400"')
        super(Location, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(APP_NAME+":location", kwargs={'pk': self.pk})


class OrganizationUnit(ProjectManagerPage):
    employer = models.ForeignKey("employer", verbose_name=_(
        "employer"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("OrganizationUnits")

    def save(self, *args, **kwargs):
        
        if 'class_name' in kwargs:
            self.class_name = kwargs['class_name']
        else:
            self.class_name = "organizationunit"
        return super(OrganizationUnit, self).save(*args, **kwargs)

    def employees(self):
        return self.employee_set.all()

    @property
    def full_title(self):
        if self.parent is None:
            return self.title
        return self.title+" " + OrganizationUnit.objects.get(pk=self.parent.id).full_title

    def childs(self):
        return OrganizationUnit.objects.filter(parent_id=self.id)


class EmployeeSpeciality(ProjectManagerPage):
    employee = models.ForeignKey("employee", verbose_name=_(
        "employee"), on_delete=models.CASCADE)
    max = models.IntegerField(_("max"))
    value = models.IntegerField(_("value"))
    percent = models.IntegerField(_("percent"))
    verified = models.BooleanField(_("verified"), default=False)

    class Meta:
        verbose_name = _("EmployeeSpeciality")
        verbose_name_plural = _("EmployeeSpecialitys")

    def save(self, *args, **kwargs):
        self.class_name = "employeespeciality"
        return super(OrganizationUnit, self).save(*args, **kwargs)

    def __str__(self):
        return f"""{self.employee} {self.title}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":employee_speciality", kwargs={"pk": self.pk})


class Request(models.Model):
    project = models.ForeignKey("Project", verbose_name=_(
        "پروژه"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("تعداد"))
    unit_name = models.CharField(
        _("واحد"), choices=UnitNameEnum.choices, default=UnitNameEnum.ADAD, max_length=50)
    unit_price = models.IntegerField(_("قیمت واحد"))
    description = models.CharField(
        _("توضیحات"), null=True, blank=True, default='', max_length=50)
    creator = models.ForeignKey("employee", related_name="request_createds", verbose_name=_(
        "ثبت کننده"), on_delete=models.PROTECT)
    handler = models.ForeignKey("employee", related_name="request_handeleds", verbose_name=_(
        "پاسخ دهنده"), null=True, blank=True, on_delete=models.PROTECT)
    date_added = models.DateTimeField(
        _("تاریخ درخواست"), auto_now=False, auto_now_add=True)
    date_delivered = models.DateTimeField(
        _("تاریخ درخواست"), null=True, blank=True, auto_now=False, auto_now_add=False)
    status = models.CharField(_("وضعیت"), choices=RequestStatusEnum.choices,
                              default=RequestStatusEnum.REQUESTED, max_length=50)
    request_type = models.CharField(
        _("type"), choices=RequestTypeEnum.choices, max_length=50)
    class_name = 'request'

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def persian_date_delivered(self):
        return PersianCalendar().from_gregorian(self.date_delivered)

    def can_be_edited(self):
        return self.project.can_be_edited

    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""

    def signatures(self):
        return RequestSignature.objects.filter(materialrequest=self).order_by('-date_added')

    def line_total(self):
        return self.quantity*self.unit_price

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    def __str__(self):
        return self.project.title

    def get_absolute_url(self):
        return reverse("Request_detail", kwargs={"pk": self.pk})


class MaterialRequest(Request):
    material = models.ForeignKey("Material", verbose_name=_(
        "متریال"), on_delete=models.PROTECT)

    class_name = 'materialrequest'

    class Meta:
        verbose_name = _("درخواست متریال")
        verbose_name_plural = _("درخواست های متریال")

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

    def save(self, *args, **kwargs):
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
        self.request_type = RequestTypeEnum.MATERIAL_REQUEST
        return super(MaterialRequest, self).save(*args, **kwargs)


class ServiceRequest(Request):
    service = models.ForeignKey("service", verbose_name=_("service"), on_delete=models.PROTECT)

    class_name = 'servicerequest'

    class Meta:
        verbose_name = _("درخواست سرویس")
        verbose_name_plural = _("درخواست های سرویس")

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

    def save(self, *args, **kwargs):
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
        self.request_type = RequestTypeEnum.SERVICE_REQUEST
        return super(ServiceRequest, self).save(*args, **kwargs)


class RequestSignature(models.Model):
    request = models.ForeignKey("request", verbose_name=_(
        "request"), on_delete=models.CASCADE)
    employee = models.ForeignKey("employee", verbose_name=_(
        "employee"), on_delete=models.PROTECT)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    description = models.CharField(_("description"), max_length=200)
    status = models.CharField(_("status"), choices=SignatureStatusEnum.choices,
                              default=SignatureStatusEnum.REQUESTED, max_length=200)

    class_name = "requestsignature"

    class Meta:
        verbose_name = _("RequestSignature")
        verbose_name_plural = _("RequestSignatures")

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""
            <span class="badge badge-{self.get_status_color()}">{self.status}</span>
        """

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("RequestSignature_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"


class WareHouse(OrganizationUnit):
    address = models.CharField(_("آدرس"), null=True, blank=True, max_length=500)

    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("WareHouses")

    def save(self, *args, **kwargs):
        self.class_name = "warehouse"
        return super(WareHouse, self).save(class_name="warehouse", *args, **kwargs)

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


class WareHouseSheet(models.Model):
    sheet_no=models.CharField(_("sheet_no"), max_length=50)
    direction=models.CharField(_("direction"),choices=WareHouseSheetDirectionEnum.choices, max_length=50)
    ware_house=models.ForeignKey("warehouse", verbose_name=_("warehouse"), on_delete=models.CASCADE)
    material=models.ForeignKey("material", verbose_name=_("material"), on_delete=models.CASCADE)
    serial_no=models.CharField(_("serial_no"),null=True,blank=True, max_length=50)
    quantity=models.IntegerField(_("quantity"))
    unit_price=models.IntegerField(_("unit_price"),default=0)
    unit_name=models.CharField(_("unit_name"),max_length=100,default="عدد")
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_entered=models.DateTimeField(_("date_entered"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_exited=models.DateTimeField(_("date_exited"),null=True,blank=True, auto_now=False, auto_now_add=False)
    employee=models.ForeignKey("employee",null=True,blank=True, verbose_name=_("employee"), on_delete=models.CASCADE)
    # who_exited=models.ForeignKey("employee",null=True,blank=True, verbose_name=_("who_entered"), on_delete=models.CASCADE)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    class Meta:
        verbose_name = _("WareHouseSheet")
        verbose_name_plural = _("WareHouseSheets")

    def __str__(self):
        return self.ware_house.title

    def get_absolute_url(self):
        return reverse("WareHouseSheet", kwargs={"pk": self.pk})
