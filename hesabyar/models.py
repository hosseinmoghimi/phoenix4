from django.db import models
from core.settings import ADMIN_URL
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from core.enums import ColorEnum
from utility.persian import PersianCalendar
from .apps import APP_NAME
from core.models import BasicPage


class HesabYarPage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(HesabYarPage,self).save(*args, **kwargs)


class FinancialYear(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    year=models.IntegerField(_("year"))
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    
    
    def __str__(self):
        return self.title


    class Meta:
        verbose_name = _("FinancialYear")
        verbose_name_plural = _("FinancialYears")


class FinancialDocument(HesabYarPage):
    financial_year=models.ForeignKey("FinancialYear", verbose_name=_("financial_year"), on_delete=models.CASCADE)
    account=models.ForeignKey("FinancialAccount",verbose_name=_("account"), on_delete=models.CASCADE)
    category=models.ForeignKey("financialdocumentcategory", verbose_name=_("category"), on_delete=models.CASCADE)
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    document_datetime=models.DateTimeField(_("document_datetime"), auto_now=False, auto_now_add=False)
    def category_title(self):
        return self.category.title
    def persian_document_datetime(self):
        return PersianCalendar().from_gregorian(self.document_datetime)
    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("FinancialDocuments")


    def save(self,*args, **kwargs):
        self.class_name='financialdocument'
        return super(FinancialDocument,self).save(*args, **kwargs)


class FinancialDocumentCategory(models.Model):
    title=models.CharField(_("دسته بندی"),max_length=100) 
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    class Meta:
        verbose_name = _("FinancialDocumentCategory")
        verbose_name_plural = _("FinancialDocumentCategories")

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        self.class_name='financialdocumentcategory'
        return super(FinancialDocumentCategory,self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(APP_NAME+":financial_document_category", kwargs={"pk": self.pk})


class Tag(models.Model):
    name=models.CharField(_("name"), max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":tag", kwargs={"pk": self.pk})


class FinancialAccount(models.Model):
    title=models.CharField(_("title"),blank=True, max_length=200)
    tags=models.ManyToManyField("tag",blank=True, verbose_name=_("برچسب ها"))
    class_name="financialaccount"
    def rest(self):
        rest=0
        for t in FinancialDocument.objects.filter(account=self):
            rest=rest-t.bedehkar
            rest=rest+t.bestankar
        return rest
    def get_absolute_url(self):
        return reverse(APP_NAME+":financial_account",kwargs={'pk':self.pk})
    class Meta:
        verbose_name = _("FinancialAccount")
        verbose_name_plural = _("FinancialAccounts")

    def __str__(self):
        return self.title 


    def save(self,*args, **kwargs):
        self.class_name='financialdocument'
        return super(FinancialAccount,self).save(*args, **kwargs)

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"
class ProfileFinancialAccount(FinancialAccount):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name='profilefinancialaccount'

    class Meta:
        verbose_name = _("ProfileFinancialAccount")
        verbose_name_plural = _("ProfileFinancialAccounts")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse("FinancialProfileAccount_detail", kwargs={"pk": self.pk})


    def save(self,*args, **kwargs):
        if self.title is None or self.title=="":
            self.title=self.profile.name
        return super(ProfileFinancialAccount,self).save(*args, **kwargs)
 

class Cash(FinancialAccount):
    store=models.ForeignKey("store", verbose_name=_("فروشگاه"), on_delete=models.CASCADE)
    class_name='cash'
    class Meta:
        verbose_name = _("Cash")
        verbose_name_plural = _("Cashes")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("FinancialProfileAccount_detail", kwargs={"pk": self.pk})


    def save(self,*args, **kwargs):
        return super(Cash,self).save(*args, **kwargs)


class BankAccount(ProfileFinancialAccount):
    bank=models.ForeignKey("bank", verbose_name=_("bank"), on_delete=models.CASCADE)
    account_no=models.CharField(_("shomareh"),null=True,blank=True, max_length=50)
    card_no=models.CharField(_("card"),null=True,blank=True, max_length=50)
    shaba_no=models.CharField(_("shaba"),null=True,blank=True, max_length=50)
    class_name='bankaccount'
    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("BankAccounts")

   

    def get_absolute_url(self):
        return reverse("FinancialProfileAccount_detail", kwargs={"pk": self.pk})


    def __str__(self):
        return self.title


    def save(self,*args, **kwargs):
        self.title=f"""حساب {self.bank} {self.profile.name}"""
        return super(BankAccount,self).save(*args, **kwargs)


class Bank(models.Model):
    name=models.CharField(_("بانک"), max_length=50)
    branch=models.CharField(_("شعبه"),null=True,blank=True, max_length=50)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("تلفن"),null=True,blank=True, max_length=50)
    
    
    def __str__(self):
        return f"""بانک {self.name}  {(("شعبه "+self.branch) or "")}"""


    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
 

class Store(models.Model):
    name=models.CharField(_("name"), max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)

    

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Store_detail", kwargs={"pk": self.pk})
