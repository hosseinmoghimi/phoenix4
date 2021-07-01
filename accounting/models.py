from django.db import models
from django.db.models import Q

from django.db.models.base import Model
from django.db.models.fields import BooleanField
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .settings import *
from django.shortcuts import reverse
from django.http import Http404
from tinymce.models import HTMLField
from .enums import *
from utility.persian import PersianCalendar
IMAGE_FOLDER = APP_NAME+'/images/'


class FinancialAccount(models.Model):
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)

    def total(self):
        total = 0
        for transaction in Transaction.objects.filter(pay_from=self):
            total += transaction.amount
        for transaction in Transaction.objects.filter(pay_to=self):
            total -= transaction.amount
        return total

    def get_transactions_url(self):
        return reverse(APP_NAME+":transactions", kwargs={'financial_account_id': self.pk})

    def transactions(self):
        return Transaction.objects.filter(Q(pay_from=self) | Q(pay_to=self)).all().order_by("date_paid")

    class Meta:
        verbose_name = _("FinancialAccount")
        verbose_name_plural = _("FinancialAccounts")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":financial_account", kwargs={"pk": self.pk})


class BankAccount(models.Model):
    title = models.CharField(_("title"), max_length=50)
    owner = models.ForeignKey("FinancialAccount", verbose_name=_(
        "owner"), on_delete=models.CASCADE)
    bank = models.CharField(
        _("bank"), choices=BankNameEnum.choices, max_length=50)
    branch = models.CharField(_("شعبه"), max_length=50)

    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("BankAccounts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("BankAccount_detail", kwargs={"pk": self.pk})


class Transaction(models.Model):
    title = models.CharField(_("title"), max_length=50)
    pay_from = models.ForeignKey("FinancialAccount", related_name="pay_from", verbose_name=_(
        "pay_from"), on_delete=models.CASCADE)
    pay_to = models.ForeignKey("FinancialAccount", related_name="pay_to", verbose_name=_(
        "pay_to"), on_delete=models.CASCADE)
    amount = models.IntegerField(_("amount"), default=0)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    date_paid = models.DateTimeField(
        _("date_paid"), auto_now=False, auto_now_add=False)
    creator = models.ForeignKey("authentication.profile", verbose_name=_(
        "ثبت کننده"), on_delete=models.CASCADE)

    def persian_date_paid(self):
        return PersianCalendar().from_gregorian(self.date_paid)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(APP_NAME+"transaction", kwargs={"pk": self.pk})
