from tinymce.models import HTMLField
from django.db import models

from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from core.enums import ColorEnum
from hesabyar.enums import InvoiceStatusEnum, WareHouseSheetDirectionEnum, WareHouseSheetStatusEnum
from utility.persian import PersianCalendar
from .apps import APP_NAME
from core.models import BasicPage

IMAGE_FOLDER=APP_NAME+"/images/"
class HesabYarPage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(HesabYarPage,self).save(*args, **kwargs)


class LinkHelper():
    
    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name,kwargs={'pk':self.pk})
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"

class FinancialYear(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    year=models.IntegerField(_("year"))
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    def get_by_date(date):
        return FinancialYear.objects.filter(start_date__lte=date).filter(end_date__gte=date).first()
    
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
        return super(FinancialDocument,self).save(*args, **kwargs)

class InvoiceFinancialDocument(FinancialDocument):
    invoice=models.ForeignKey("invoice", verbose_name=_("invoice"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("InvoiceFinancialDocument")
        verbose_name_plural = _("InvoiceFinancialDocuments")

    def save(self,*args, **kwargs):
        self.class_name="invoicefinancialdocument"
        super(InvoiceFinancialDocument,self).save(*args, **kwargs)
 


class PaymentFinancialDocument(FinancialDocument):
    payment=models.ForeignKey("payment", verbose_name=_("payment"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("PaymentFinancialDocument")
        verbose_name_plural = _("PaymentFinancialDocuments")

    def save(self,*args, **kwargs):
        self.class_name="paymentfinancialdocument"
        super(PaymentFinancialDocument,self).save(*args, **kwargs)

 

class ProductOrService(HesabYarPage):
    

    class Meta:
        verbose_name = _("ProductOrService")
        verbose_name_plural = _("ProductOrServices")

    def save(self,*args, **kwargs):
        return super(ProductOrService,self).save(*args, **kwargs)
 

class Product(ProductOrService):
    
    def available(self):
        aa=0
        for sheet in WareHouseSheet.objects.filter(status=WareHouseSheetStatusEnum.DONE).filter(product=self):
            if sheet.direction==WareHouseSheetDirectionEnum.ENTER:
                aa+=sheet.quantity
            if sheet.direction==WareHouseSheetDirectionEnum.EXIT:
                aa-=sheet.quantity
        return aa

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self,*args, **kwargs):
        self.class_name="product"
        return super(Product,self).save(*args, **kwargs)
 
class Service(ProductOrService):
    

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def save(self,*args, **kwargs):
        self.class_name="service"
        return super(Service,self).save(*args, **kwargs)

class Invoice(models.Model,LinkHelper):
    status=models.CharField(_("وضعیت"),choices=InvoiceStatusEnum.choices,default=InvoiceStatusEnum.DRAFT, max_length=50)
    customer=models.ForeignKey("profilefinancialaccount", null=True,blank=True,verbose_name=_("مشتری"), on_delete=models.SET_NULL)
    seller=models.ForeignKey("store", verbose_name=_("فروشنده"), on_delete=models.CASCADE)
    tax_percent=models.IntegerField(_("درصد مالیات"),default=9)
    invoice_datetime=models.DateTimeField(_("تاریخ فاکتور"), auto_now=False, auto_now_add=False)
    date_added=models.DateTimeField(_("تاریخ ثبت"), auto_now=False, auto_now_add=True)
    ship_fee=models.IntegerField(_("هزینه حمل"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
    description=HTMLField(_("توضیحات"),max_length=50000,blank=True,null=True)
    class_name='invoice'
    @property
    def title(self):
        try:

            return "فاکتور شماره "+str(self.pk)
        except:
            return "فاکتور شماره 0"
    def persian_invoice_datetime(self):
        return PersianCalendar().from_gregorian(self.invoice_datetime)
    def tax_amount(self):
        
        sum=self.lines_total()
        sum+=self.ship_fee
        return int(self.tax_percent*sum/100.0)

    def lines_total(self):
        sum=0
        for li in self.invoice_lines():
            sum+=int(li.quantity*li.unit_price)
        return sum
    def sum_total(self):
        sum=self.lines_total()
        sum+=self.ship_fee
        sum+=((sum*self.tax_percent)/100.0)
        sum-=self.discount
        return sum
    def save(self,*args, **kwargs):
        super(Invoice,self).save(*args, **kwargs)
        # financial_year=FinancialYear.get_by_date(date=self.invoice_datetime)
        # FinancialDocumentCategory.objects.get_or_create(title="فروش")
        # category=FinancialDocumentCategory.objects.get(title="فروش")
        # InvoiceFinancialDocument.objects.filter(invoice=self).delete()

        # ifd1=InvoiceFinancialDocument()
        # ifd1.financial_year=financial_year
        # ifd1.category=category
        # ifd1.account=self.customer
        # ifd1.invoice=self
        # ifd1.bedehkar=self.sum_total()
        # ifd1.title=str(self)
        # ifd1.document_datetime=self.invoice_datetime
        # ifd1.save()

        # ifd1=InvoiceFinancialDocument()
        # ifd1.bestankar=self.sum_total()
        # ifd1.invoice=self
        # ifd1.title=str(self)
        # ifd1.financial_year=financial_year
        # ifd1.category=category
        # ifd1.document_datetime=self.invoice_datetime
        # ifd1.account=self.seller.owner
        # ifd1.save()
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
    def __str__(self):
        return self.title
    # def save(self,*args, **kwargs):
    #     self.class_name='invoice'
    #     return super(Invoice,self).save(*args, **kwargs)
 
    def invoice_lines(self):
        return InvoiceLine.objects.filter(invoice=self).order_by('row')

class InvoiceLine(models.Model):
    invoice=models.ForeignKey("invoice", verbose_name=_("invoice"), on_delete=models.CASCADE)
    row=models.IntegerField(_("row"))
    productorservice=models.ForeignKey("productorservice", verbose_name=_("productorservice"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    unit_price=models.IntegerField(_("unit_price"))
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    def save(self,*args, **kwargs):
        super(InvoiceLine,self).save(*args, **kwargs)
        self.invoice.save()
    class Meta:
        verbose_name = _("InvoiceLine")
        verbose_name_plural = _("InvoiceLines")

    def __str__(self):
        return f"{self.invoice} {self.row} - {self.productorservice.title} "

    def get_absolute_url(self):
        return reverse("InvoiceLine_detail", kwargs={"pk": self.pk})

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
    class_name=models.CharField(_("class_name"), max_length=50)
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
        # self.class_name='financialdocument'
        return super(FinancialAccount,self).save(*args, **kwargs)

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"

class ProfileFinancialAccount(FinancialAccount):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ProfileFinancialAccount")
        verbose_name_plural = _("ProfileFinancialAccounts")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":profile_financial_account", kwargs={"pk": self.pk})


    def save(self,*args, **kwargs):
        if self.title is None or self.title=="":
            self.title=self.profile.name
        self.class_name='profilefinancialaccount'
        
        return super(ProfileFinancialAccount,self).save(*args, **kwargs)
 

class Cash(FinancialAccount):
    store=models.ForeignKey("store", verbose_name=_("فروشگاه"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Cash")
        verbose_name_plural = _("Cashes")
 

    def save(self,*args, **kwargs):
        self.class_name="cash"
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
        return reverse(APP_NAME+":bank_account", kwargs={"pk": self.pk})


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
 

class Store(HesabYarPage):
    logo_origin=models.ImageField(_("logo"),null=True,blank=True, upload_to=IMAGE_FOLDER+"store/", height_field=None, width_field=None, max_length=None)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    bank_account=models.ForeignKey("bankaccount",related_name="stores",null=True,blank=True, verbose_name=_("bankaccount"), on_delete=models.CASCADE)
    owner=models.ForeignKey("profilefinancialaccount", verbose_name=_("owner"), on_delete=models.CASCADE)
    
    def logo(self):
        if self.logo_origin:
            return MEDIA_URL+str(self.logo_origin)
        else:
            return STATIC_URL+APP_NAME+"/img/store/logo.png"
    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    def save(self,*args, **kwargs):
        self.class_name="store"
        return super(Store,self).save(*args, **kwargs)


class WareHouse(HesabYarPage):
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    owner=models.ForeignKey("profilefinancialaccount", verbose_name=_("owner"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("WareHouses")

    def save(self,*args, **kwargs):
        self.class_name="warehouse"
        return super(WareHouse,self).save(*args, **kwargs)


class WareHouseSheet(models.Model,LinkHelper):
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_registered=models.DateTimeField(_("date_registered"), auto_now=False, auto_now_add=False)
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)    
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)    
    quantity=models.IntegerField(_("quantity"))
    direction=models.CharField(_("direction"),choices=WareHouseSheetDirectionEnum.choices, max_length=50)
    ware_house=models.ForeignKey("warehouse", verbose_name=_("ware_house"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=WareHouseSheetStatusEnum.choices,default=WareHouseSheetStatusEnum.INITIAL, max_length=50)
    description=HTMLField(_("description"),null=True,blank=True,max_length=50000)
    class_name="warehousesheet"
    class Meta:
        verbose_name = _("WareHouseSheet")
        verbose_name_plural = _("WareHouseSheets")
    def persian_date_registered(self):
        return PersianCalendar().from_gregorian(self.date_registered)

    def save(self,*args, **kwargs):
        self.class_name="warehousesheet"
        super(WareHouseSheet,self).save(*args, **kwargs)


class Payment(models.Model,LinkHelper):
    title=models.CharField(_("title"),default='پرداخت', max_length=50)
    pay_from=models.ForeignKey("financialaccount",related_name="paid_set", verbose_name=_("pay_from"), on_delete=models.CASCADE)
    pay_to=models.ForeignKey("financialaccount",related_name="received_set", verbose_name=_("pay_to"), on_delete=models.CASCADE)
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)
    amount=models.IntegerField(_("amount"))
    date_paid=models.DateTimeField(_("date_paid"), auto_now=False, auto_now_add=False)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name="payment"
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def save(self,*args, **kwargs):
        super(Payment,self).save(*args, **kwargs)
        financial_year=FinancialYear.get_by_date(date=self.date_paid)
        FinancialDocumentCategory.objects.get_or_create(title="واریز")
        category=FinancialDocumentCategory.objects.get(title="واریز")
        PaymentFinancialDocument.objects.filter(payment=self).delete()

        ifd1=PaymentFinancialDocument()
        ifd1.financial_year=financial_year
        ifd1.category=category
        ifd1.account=self.pay_to
        ifd1.payment=self
        ifd1.bedehkar=self.amount
        ifd1.title=str(self)
        ifd1.document_datetime=self.date_paid
        ifd1.save()

        ifd1=PaymentFinancialDocument()
        ifd1.bestankar=self.amount
        ifd1.payment=self
        ifd1.title=str(self)
        ifd1.financial_year=financial_year
        ifd1.category=category
        ifd1.document_datetime=self.date_paid
        ifd1.account=self.pay_from
        ifd1.save()