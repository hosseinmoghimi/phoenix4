from core.models import BasicPage
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
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


class AccountingPage(BasicPage):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(AccountingPage,self).save(*args, **kwargs)


class Asset(models.Model):
    app_name=models.CharField(_("app_name"),blank=True, max_length=50)
    class_name=models.CharField(_("class_name"),blank=True, max_length=50)
    title=models.CharField(_("title"), max_length=50)
    price=models.IntegerField(_("price"),default=0)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    year=models.IntegerField(_("سال ساخت"))
    image_origin=models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"Property",null=True,blank=True, height_field=None, width_field=None, max_length=None)
    owner=models.CharField(_("مالک"), max_length=50,null=True,blank=True)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now=True, auto_now_add=False)
    description=HTMLField(_("توضیحات"),null=True,blank=True, max_length=5000)
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)

    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("دارایی ها")

    def __str__(self):
        return self.title
    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
    def get_absolute_url(self):
        return reverse(self.app_name+":"+self.class_name, kwargs={self.class_name+"_id": self.pk})
    def get_edit_btn(self):
        return f"""
        <a href="{self.get_edit_url()}" target="_blank">
      <i class="material-icons">
          edit
      </i>
  </a>
        """


class FinancialAccount(models.Model):
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)
    def get_by_profile_or_new(profile_id):
        fa=FinancialAccount.objects.filter(profile_id=profile_id).first()
        if fa is None:
            fa=FinancialAccount(profile_id=profile_id)
            fa.save()
        return fa

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
        verbose_name_plural = _("حساب های مالی")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":financial_account", kwargs={"financial_account_id": self.pk})


class BankAccount(models.Model):
    title = models.CharField(_("عنوان"), max_length=50)
    owner = models.ForeignKey("FinancialAccount", verbose_name=_(
        "صاحب حساب"), on_delete=models.CASCADE)
    bank = models.CharField(
        _("بانک"), choices=BankNameEnum.choices, max_length=50)
    branch = models.CharField(_("شعبه"), max_length=50)
    account_no=models.CharField(_("شماره حساب"), null=True,blank=True,max_length=50)
    card_no=models.CharField(_("شماره کارت"), null=True,blank=True,max_length=50)
    shaba_no=models.CharField(_("شماره شبا"), null=True,blank=True,max_length=50)
    class_name="bankaccount"
    description=HTMLField(_("description"),null=True,blank=True, max_length=5000)
    is_active=models.BooleanField(_("is active ?"),default=True)
    is_default=models.BooleanField(_("is default ?"),default=True)
    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("حساب های بانکی")
    def to_html(bank_account):
        desc="شماره حساب "
        if bank_account.bank is not None:
            desc=f"{desc} {bank_account.bank}"
        if bank_account.owner is not None:
            desc=f"{desc} ، به&nbsp;نام&nbsp;{bank_account.owner.profile.name}"
        if bank_account.card_no is not None:
            desc=f"{desc} ، شماره&nbsp;کارت&nbsp;{bank_account.card_no}"
        if bank_account.shaba_no is not None:
            desc=f"{desc} ، شماره&nbsp;شبا&nbsp;{bank_account.shaba_no}"
        if bank_account.account_no is not None:
            desc=f"{desc} ، شماره&nbsp;حساب&nbsp;{bank_account.account_no}"
        return desc

        
    def __str__(bank_account):
        desc="شماره حساب "
        if bank_account.bank is not None:
            desc=f"{desc} {bank_account.bank}"
        if bank_account.owner is not None:
            desc=f"{desc} ، به نام {bank_account.owner.profile.name}"
        if bank_account.card_no is not None:
            desc=f"{desc} ، شماره کارت {bank_account.card_no}"
        if bank_account.shaba_no is not None:
            desc=f"{desc} ، شماره شبا {bank_account.shaba_no}"
        if bank_account.account_no is not None:
            desc=f"{desc} ، شماره حساب {bank_account.account_no}"
        return desc
    def get_absolute_url(self):
        return self.owner.get_absolute_url()


    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


class Transaction(AccountingPage):
    pay_from = models.ForeignKey("FinancialAccount", related_name="pay_from_set", verbose_name=_(
        "pay_from"), on_delete=models.CASCADE)
    pay_to = models.ForeignKey("FinancialAccount", related_name="pay_to_set", verbose_name=_(
        "pay_to"), on_delete=models.CASCADE)
    amount = models.IntegerField(_("amount"), default=0)
    date_paid = models.DateTimeField(
        _("date_paid"), auto_now=False, auto_now_add=False)
    rest=0
    direction=None 
    def asset(self):
        ooo=AssetTransaction.objects.filter(pk=self.pk).first()
        if ooo is not None:
            return ooo.asset

    def order(self):
        ooo=MarketOrderTransaction.objects.filter(pk=self.pk).first()
        if ooo is not None:
            return ooo.order

    def project(self):
        ooo=ProjectTransaction.objects.filter(pk=self.pk).first()
        if ooo is not None:
            return ooo.project


    def payment_method(self):
        ooo=MoneyTransaction.objects.filter(pk=self.pk).first()
        if ooo is not None:
            return ooo.payment_method

    def save(self,*args, **kwargs):
        return super(Transaction,self).save(*args, **kwargs)
    def get_icon(self):
        return self.get_sub_transaction().get_icon()
    def get_color(self):
        if self.direction:
            return "success"
        if not self.direction:
            return "danger"
    def get_transaction2_url(self):
        return reverse(APP_NAME+":transactions2",kwargs={'pay_to_id':self.pay_to.id,'pay_from_id':self.pay_from.id})
    def calculate_direction(self,financial_account_id):
        if self.pay_from.id==financial_account_id:
            self.direction=True 
        if self.pay_to.id==financial_account_id:
            self.direction=False
        return self.direction
    def calculate_rest(self,pay_to_id,pay_from_id):
        self.calculate_direction(financial_account_id=pay_from_id)
        list1=Transaction.objects.filter(pay_to__id=pay_to_id).filter(pay_from__id=pay_from_id).filter(date_paid__lte=self.date_paid)
        list2=Transaction.objects.filter(pay_to__id=pay_from_id).filter(pay_from__id=pay_to_id).filter(date_paid__lte=self.date_paid)
        self.rest=0
        for i in list1:
            self.rest+=i.amount
        for i in list2:
            self.rest-=i.amount
        return self.rest



    def get_sub_transaction(self):
        at=AssetTransaction.objects.filter(pk=self.pk).first()
        if at is not None:
            return at
        pt=ProjectTransaction.objects.filter(pk=self.pk).first()
        if pt is not None:
            return pt
        mt=MoneyTransaction.objects.filter(pk=self.pk).first()
        if mt is not None:
            return mt
        mot=MarketOrderTransaction.objects.filter(pk=self.pk).first()
        if mot is not None:
            return mot


    def persian_date_paid(self):
        return PersianCalendar().from_gregorian(self.date_paid)

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("تراکنش ها")

    def __str__(self):
        return self.title
 
 
    def get_absolute_url(self):
        # mt=MoneyTransaction.objects.filter(pk=self.pk)
        # ot=MarketOrderTransaction.objects.filter(pk=self.pk)
        # at=AssetTransaction.objects.filter(pk=self.pk)
        return self.get_sub_transaction().get_absolute_url()

    def get_edit_url(self):
        return self.get_sub_transaction().get_edit_url()

 
class AssetTransaction(Transaction):
    asset = models.ForeignKey("asset", verbose_name=_("asset"), on_delete=models.CASCADE)
    
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name,kwargs={'pk':self.pk})


    class Meta:
        verbose_name = _("AssetTransaction")
        verbose_name_plural = _("انتقال دارایی ها")

    def save(self,*args, **kwargs):
        self.class_name="assettransaction"
        return super(AssetTransaction,self).save(*args, **kwargs)
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_icon(self):
        type1="پول"
        color="success"
        if self.class_name=="marketordertransaction":
            type1="سفارش"
            color="primary"
        if self.class_name=="assettransaction":
            type1="دارایی"
            color="warning"
        if self.class_name=="moneytransaction":
            type1="پول"
            color="success"
        return f"""
            <span class="badge badge-{color}">
            {type1}
            </span>
            """


class MarketOrderTransaction(Transaction):
    order=models.ForeignKey("market.order", verbose_name=_("order"), on_delete=models.CASCADE)

        
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name,kwargs={'pk':self.pk})

    def save(self,*args, **kwargs):
        self.class_name="marketordertransaction"
        return super(MarketOrderTransaction,self).save(*args, **kwargs)
    class Meta:
        verbose_name = _("MarketOrderTransaction")
        verbose_name_plural = _("تراکنش های صورت حساب فروش")
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"


    def get_icon(self):
        type1="پول"
        color="success"
        if self.class_name=="marketordertransaction":
            type1="سفارش"
            color="primary"
        if self.class_name=="assettransaction":
            type1="دارایی"
            color="warning"
        if self.class_name=="moneytransaction":
            type1="پول"
            color="success"
        return f"""
            <span class="badge badge-{color}">
            {type1}
            </span>
            """


class ProjectTransaction(Transaction):
    project=models.ForeignKey("projectmanager.project", verbose_name=_("project"), on_delete=models.CASCADE)

        
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name,kwargs={'pk':self.pk})

    def save(self,*args, **kwargs):
        self.class_name="projecttransaction"
        return super(ProjectTransaction,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("ProjectTransaction")
        verbose_name_plural = _("تراکنش های پروژه ها")
        
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

    def __str__(self):
        return f"""بابت حساب پروژه - {self.project.title}"""
    def get_icon(self):
        type1="پروژه"
        color="danger" 
        return f"""
            <span class="badge badge-{color}">
            {type1}
            </span>
            """


class MoneyTransaction(Transaction):
    payment_method=models.CharField(_("payment_method"),choices=PaymetMethodEnum.choices,default=PaymetMethodEnum.CARD, max_length=50)

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name,kwargs={'pk':self.pk})

    def get_icon(self):
        type1="پول"
        color="success"
        if self.class_name=="marketordertransaction":
            type1="سفارش"
            color="primary"
        if self.class_name=="assettransaction":
            type1="دارایی"
            color="warning"
        if self.class_name=="moneytransaction":
            type1="پول"
            color="success"
        return f"""
            <span class="badge badge-{color}">
            {type1}
            </span>
            """
    class Meta:
        verbose_name = _("MoneyTransaction")
        verbose_name_plural = _("تراکنش های پولی")

    def save(self,*args, **kwargs):
        self.class_name="moneytransaction"
        return super(MoneyTransaction,self).save(*args, **kwargs)
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"