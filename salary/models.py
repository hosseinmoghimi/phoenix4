from projectmanager.repo import Employee
from core.models import BasicPage
from django.db import models
from django.shortcuts import reverse
from utility.persian import PERSIAN_MONTH_NAMES, PersianCalendar
from core.settings import ADMIN_URL
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .settings import *
from .enums import *


class SalaryPage(BasicPage):

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(SalaryPage, self).save(*args, **kwargs)


class Vacation(SalaryPage): 
    vacation_started=models.DateTimeField(_("vacation_started"), auto_now=False, auto_now_add=False)
    vacation_ended=models.DateTimeField(_("vacation_ended"),null=True,blank=True, auto_now=False, auto_now_add=False)
    employee = models.ForeignKey("projectmanager.employee", verbose_name=_(
        "employee"), on_delete=models.CASCADE)
    class_name = "vacation"

    def persian_vacation_started(self):
        return PersianCalendar().from_gregorian(self.vacation_started)
    def persian_vacation_ended(self):
        return PersianCalendar().from_gregorian(self.vacation_ended)

    def save(self, *args, **kwargs):
        self.class_name = "vacation"
        return super(Vacation, self).save(*args, **kwargs)


    class Meta:
        verbose_name = _("Vacation")
        verbose_name_plural = _("Vacations")



class EmployeeSalary(models.Model):
    employee = models.ForeignKey("projectmanager.employee", verbose_name=_(
        "employee"), on_delete=models.CASCADE)
    year = models.IntegerField(_("سال"))
    month = models.IntegerField(_("ماه"))
    month_name = models.CharField(_("ماه"), max_length=50)
    date_added = models.DateTimeField(
        _("تاریخ ثبت"), auto_now=False, auto_now_add=True)
    date_paid = models.DateTimeField(
        _("تاریخ واریز"), auto_now=False, auto_now_add=False)

    class_name = "employeesalary"

    def save(self, *args, **kwargs):
        if not ((self.month)-1) in range(12):
            self.month = 1
        self.month_name = PERSIAN_MONTH_NAMES[self.month-1]
        return super(EmployeeSalary, self).save(*args, **kwargs)
    def get_print_url(self):
        return reverse(APP_NAME+":print",kwargs={'pk':self.pk})
    class Meta:
        verbose_name = _("EmployeeSalary")
        verbose_name_plural = _("EmployeeSalarys")

    def lines(self):
        return SalaryLine.objects.filter(employee_salary=self)

    def negative_lines(self):
        return SalaryLine.objects.filter(employee_salary=self).filter(direction=SalaryDirectionEnum.KOSURAT)

    def positive_lines(self):
        return SalaryLine.objects.filter(employee_salary=self).filter(direction=SalaryDirectionEnum.MAZAYA)

    def total_positives(self):
        sum = 0
        for line in self.positive_lines():
            sum += line.amount
        return sum

    def total_negatives(self):
        sum = 0
        for line in self.negative_lines():
            sum += line.amount
        return sum

    def __str__(self):
        return f"{self.employee.profile.name} @ {self.year} : {self.month_name}"

    def total(self):

        return self.total_positives()-self.total_negatives()

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


class SalaryLine(models.Model):
    employee_salary = models.ForeignKey("employeesalary", verbose_name=_(
        "employeesalary"), on_delete=models.PROTECT)
    direction = models.CharField(_("جهت"), choices=SalaryDirectionEnum.choices,
                                 default=SalaryDirectionEnum.MAZAYA, max_length=50)
    title = models.CharField(
        _("عنوان"), choices=SalaryTitleEnum.choices, max_length=50)
    amount = models.IntegerField(_("مبلغ"))
    date_added = models.DateTimeField(
        _("تاریخ ثبت"), auto_now=False, auto_now_add=True)
    description = models.CharField(
        _("توضیحات"), null=True, blank=True, max_length=50)
    class_name = "salaryline"

    class Meta:
        verbose_name = _("SalaryLine")
        verbose_name_plural = _("SalaryLines")

    def __str__(self):
        return f"{self.employee_salary} : {self.title}"

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons text-warning">
                    edit
                </i>
            </a>
        """
    def can_be_deleted(self):
        return True

    def get_delete_btn(self):
        return f"""
             <a href="{self.get_delete_url()}" target="_blank" title="حذف">
                <i class="material-icons text-danger">
                    delete_forever
                </i>
            </a>
        """


class WorkGroup(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    organization_units=models.ManyToManyField("projectmanager.organizationunit",blank=True, verbose_name=_("واحد های سازمانی"))
    employees_origin=models.ManyToManyField("projectmanager.employee",blank=True, verbose_name=_("employees"))
    
    class_name="workgroup"
    def employees(self):
        l=[]
        for em in self.employees_origin.all():
            l.append(em.pk)
        for org in self.organization_units.all():
            for em in org.employee_set.all():
                l.append(em.pk)
        
        return Employee.objects.filter(id__in=l)

    class Meta:
        verbose_name = _("WorkGroup")
        verbose_name_plural = _("WorkGroups")

    def __str__(self):
        return self.title

   
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons text-warning">
                    edit
                </i>
            </a>
        """
    def can_be_deleted(self):
        return True

    def get_delete_btn(self):
        return f"""
             <a href="{self.get_delete_url()}" target="_blank" title="حذف">
                <i class="material-icons text-danger">
                    delete_forever
                </i>
            </a>
        """



class WorkSite(models.Model):
    parent=models.ForeignKey("worksite",null=True,blank=True, verbose_name=_("والد"), on_delete=models.CASCADE) 
    title=models.CharField(_("عنوان"), max_length=50)
    location=models.ForeignKey("map.location",null=True,blank=True, verbose_name=_("location"), on_delete=models.CASCADE)
    class_name="worksite"
    class Meta:
        verbose_name = _("WorkSite")
        verbose_name_plural = _("WorkSites")
    def childs(self):
        return WorkSite.objects.filter(parent=self)
    @property
    def full_title(self):
        if self.parent is None:
            return self.title
        else:
            return self.parent.full_title+" / "+self.title

    def __str__(self):
        return self.full_title

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons text-warning">
                    edit
                </i>
            </a>
        """
    def can_be_deleted(self):
        return True

    def get_delete_btn(self):
        return f"""
             <a href="{self.get_delete_url()}" target="_blank" title="حذف">
                <i class="material-icons text-danger">
                    delete_forever
                </i>
            </a>
        """



class WorkDay(models.Model):
    work_site=models.ForeignKey("worksite",null=True,blank=True, verbose_name=_("محل کار"), on_delete=models.CASCADE)
    work_group=models.ForeignKey("workgroup", verbose_name=_("گروه کاری"), on_delete=models.CASCADE)
    work_date=models.DateField(_("روز"), auto_now=False, auto_now_add=False)
    work_start=models.TimeField(_("ورود"), auto_now=False, auto_now_add=False)
    work_end=models.TimeField(_("خروج"), auto_now=False, auto_now_add=False)
    
    class_name="workday"
    
    def persian_work_date(self):
        return PersianCalendar().from_gregorian(self.work_date)[:10]
    # def persian_work_start(self):
    #     return PersianCalendar().from_gregorian(self.work_start)
    # def persian_work_end(self):
    #     return PersianCalendar().from_gregorian(self.work_end)

    class Meta:
        verbose_name = _("WorkDay")
        verbose_name_plural = _("WorkDays")

    def __str__(self):
        return f"""{self.work_group.title} @ {self.persian_work_date()} , {self.work_start}~{self.work_end}"""
 
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons text-warning">
                    edit
                </i>
            </a>
        """
    def can_be_deleted(self):
        return True

    def get_delete_btn(self):
        return f"""
             <a href="{self.get_delete_url()}" target="_blank" title="حذف">
                <i class="material-icons text-danger">
                    delete_forever
                </i>
            </a>
        """


class Attendance(models.Model):
    work_day=models.ForeignKey("workday", verbose_name=_("work_day"), on_delete=models.CASCADE)
    employee=models.ForeignKey("projectmanager.employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    date_entered=models.DateTimeField(_("ورود"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_exited=models.DateTimeField(_("خروج"),null=True,blank=True, auto_now=False, auto_now_add=False)
    
    class_name="attendance"
    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    def persian_date_entered(self):
        return PersianCalendar().from_gregorian(self.date_entered)
    def persian_date_exited(self):
        return PersianCalendar().from_gregorian(self.date_exited)
    def __str__(self):
        return f"""{self.employee.profile.name} , {self.work_day} , {self.date_entered.time()}~{self.date_exited.time()}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"""

    def get_delete_url(self):
        return f"""{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"""

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons text-warning">
                    edit
                </i>
            </a>
        """
    def can_be_deleted(self):
        return True

    def get_delete_btn(self):
        return f"""
             <a href="{self.get_delete_url()}" target="_blank" title="حذف">
                <i class="material-icons text-danger">
                    delete_forever
                </i>
            </a>
        """

