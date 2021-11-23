from core import apps
from core.settings import ADMIN_URL, MEDIA_URL
from django.db import models
from django.shortcuts import reverse
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext as _
from utility.persian import PersianCalendar
from .enums import PaymentTypeEnum
from .apps import APP_NAME
IMAGE_FOLDER = APP_NAME+'/img/'
# Create your models here.


class Stock(models.Model):
    profile = models.ForeignKey("authentication.profile", related_name="stock_set", verbose_name=_(
        "profile"), on_delete=models.CASCADE)
    father_name = models.CharField(
        _("نام پدر"), null=True, blank=True, max_length=50)
    agent = models.ForeignKey("agent", verbose_name=_(
        "agent"), on_delete=models.CASCADE)
    stock1 = models.IntegerField(_("stock1"), default=0)
    stock2 = models.IntegerField(_("stock2"), default=0)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("date_updated"), auto_now=True, auto_now_add=False)
    account_no = models.CharField(
        _("شماره حساب"), null=True, blank=True, max_length=50)
    melli_code = models.CharField(
        _("کد ملی"), null=True, blank=True, max_length=50)
    sh_sh = models.CharField(
        _("شماره شناسنامه"), null=True, blank=True, max_length=50)
    address = models.CharField(
        _("آدرس"), null=True, blank=True, max_length=100)
    description = models.TextField(_("توضیحات"), null=True, blank=True)
    class_name = "stock"

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_stock_amount(self):
        from core.repo import ParameterRepo
        from .enums import ParametersEnum
        param=ParameterRepo(app_name=APP_NAME)
        STOCK1=param.get(ParametersEnum.STOCK1).value
        STOCK2=param.get(ParametersEnum.STOCK2).value
        if self.stock1>0 and self.stock2>0:
            return f"{self.stock1} {STOCK1} و {self.stock2} {STOCK2}"
        if self.stock1>0 and self.stock2==0:
            return f"{self.stock1} {STOCK1}"
        if self.stock1==0 and self.stock2>0:
            return f"{self.stock2} {STOCK2}"
        return ""
    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":stock", kwargs={"pk": self.pk})

    def get_edit_btn(self):
        return f"""
            <a target="_blank" href="{self.get_edit_url()}">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """


class Agent(models.Model):
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)
    father_name = models.CharField(
        _("نام پدر"), null=True, blank=True, max_length=50)
    
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("date_updated"), auto_now=True, auto_now_add=False)
    account_no = models.CharField(
        _("شماره حساب"), null=True, blank=True, max_length=50)
    melli_code = models.CharField(
        _("کد ملی"), null=True, blank=True, max_length=50)
    sh_sh = models.CharField(
        _("شماره شناسنامه"), null=True, blank=True, max_length=50)
    address = models.CharField(
        _("آدرس"), null=True, blank=True, max_length=100)
    description = models.TextField(_("توضیحات"), null=True, blank=True)
    class_name = "agent"

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    
    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":agent", kwargs={"agent_id": self.pk})

    def get_edit_btn(self):
        return f"""
            <a target="_blank" href="{self.get_edit_url()}">
                <i class="material-icons">
                    edit
                </i>
            </a>
        """



class Payment(models.Model):
    stock = models.ForeignKey("stock", verbose_name=_(
        "stock"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    value = models.IntegerField(_("value"), default=0)
    image_origin = models.ImageField(
        _("image"), null=True, blank=True, upload_to=IMAGE_FOLDER+"Payment", max_length=100)
    date_paid = models.DateTimeField(
        _("date paid"), auto_now=False, auto_now_add=False)
    payment_type = models.CharField(
        _("payment type"), choices=PaymentTypeEnum.choices, default=PaymentTypeEnum.CASH, max_length=50)
    class_name = "payment"

    def image(self):
        if self.image_origin is not None:
            return MEDIA_URL+str(self.image_origin)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

    def __str__(self):
        return f'{self.stock.profile} : {self.title} : {self.value}'

    def persian_date_paid(self):
        return PersianCalendar().from_gregorian(self.date_paid)

    def get_absolute_url(self):
        return reverse(APP_NAME+":payment", kwargs={"pk": self.pk})


class Document(models.Model):
    stock = models.ForeignKey("stock", verbose_name=_(
        "stock"), on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    file = models.FileField(_("file"), null=True, blank=True,
                            upload_to=IMAGE_FOLDER+"Document", max_length=100)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    class_name = "document"

    def get_download_url(self):
        return reverse(APP_NAME+":get_download_response", kwargs={'pk': self.pk})

    def get_image(self):
        if self.file is not None:
            return MEDIA_URL+str(self.file)

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self):
        return f'{self.stock.profile} : {self.title}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":document", kwargs={"pk": self.pk})
