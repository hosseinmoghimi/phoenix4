
from django.db.models.fields import CharField
from core.models import BasicPage
from django.db import models
from django.shortcuts import reverse
from utility.persian import PERSIAN_MONTH_NAMES
from core.settings import ADMIN_URL, STATIC_URL
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .settings import *
from .enums import *


class SalaryPage(BasicPage):

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(SalaryPage, self).save(*args, **kwargs)


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

    def get_edit_btn(self):
        return f"""
             <a href="{self.get_edit_url()}" target="_blank" title="ویرایش">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """
