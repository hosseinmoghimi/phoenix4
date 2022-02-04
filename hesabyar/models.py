from django.db import models
from django.db.models.fields import CharField
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from core.models import BasicPage

class HesabYarPage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(HesabYarPage,self).save(*args, **kwargs)
 
class FinancialDocument(HesabYarPage):
    financial_year=models.ForeignKey("FinancialYear", verbose_name=_("financial_year"), on_delete=models.CASCADE)
    account=models.ForeignKey("FinancialAccount",verbose_name=_("account"), on_delete=models.CASCADE)
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("FinancialDocuments")


    def save(self,*args, **kwargs):
        self.class_name='financialdocument'
        return super(HesabYarPage,self).save(*args, **kwargs)
 

class FinancialAccount(models.Model):
    title=models.CharField(_("title"),blank=True, max_length=200)
    
    

    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("FinancialDocuments")

    def __str__(self):
        return self.title 


    def save(self,*args, **kwargs):
        self.class_name='financialdocument'
        return super(FinancialAccount,self).save(*args, **kwargs)
 
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

class EmployerFinancialAccount(FinancialAccount):
    employer=models.ForeignKey("projectmanager.employer", verbose_name=_("employer"), on_delete=models.CASCADE)
    class_name='employerfinancialaccount'

    class Meta:
        verbose_name = _("EmployerFinancialAccount")
        verbose_name_plural = _("EmployerFinancialAccounts")

    def __str__(self):
        return self.employer.title

    def get_absolute_url(self):
        return reverse("FinancialProfileAccount_detail", kwargs={"pk": self.pk})


    def save(self,*args, **kwargs):
        if self.title is None or self.title=="":
            self.title=self.employer.name
        return super(EmployerFinancialAccount,self).save(*args, **kwargs)

class Cash(FinancialAccount):

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
    branch=models.CharField(_("branch"),null=True,blank=True, max_length=50)
    shomare=models.CharField(_("shomareh"),null=True,blank=True, max_length=50)
    card=models.CharField(_("card"),null=True,blank=True, max_length=50)
    shaba=models.CharField(_("shaba"),null=True,blank=True, max_length=50)
    class_name='bankaccount'
    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("BankAccounts")

   

    def get_absolute_url(self):
        return reverse("FinancialProfileAccount_detail", kwargs={"pk": self.pk})


    def __str__(self):
        return self.title


    def save(self,*args, **kwargs):
        self.title=f"""حساب {self.bank.name}  {(self.branch or "")} {self.profile.name}"""
        return super(BankAccount,self).save(*args, **kwargs)

class FinancialYear(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    
    
    def __str__(self):
        return self.title


    class Meta:
        verbose_name = _("FinancialYear")
        verbose_name_plural = _("FinancialYears")
 
class Bank(models.Model):
    name=models.CharField(_("عنوان"), max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    
    
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
 
