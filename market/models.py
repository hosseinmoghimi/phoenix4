from market.enums import OrderStatusEnum
from django.db import models
from core.models import BasicPage
from .apps import APP_NAME
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.constants import CURRENCY

class MarketPage(BasicPage):

    

    class Meta:
        verbose_name = _("MarketPage")
        verbose_name_plural = _("MarketPages")

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        super(MarketPage,self).save(*args, **kwargs)

class UnitName(models.Model):
    name=models.CharField(_("unit_name"), max_length=50)
    

    class Meta:
        verbose_name = _("UnitName")
        verbose_name_plural = _("UnitNames")

    def __str__(self):
        return self.name
      
class Product(MarketPage):
    unit_names=models.ManyToManyField("unitname", verbose_name=_("unit_names"))
    for_category=models.BooleanField(_("نمایش در صفحه دسته بندی"))
    def old_price(self):
        old_price= Shop.objects.filter(product=self).order_by('-old_price').first()
        if old_price is None:
            return 0
        else:
            return old_price.old_price
    def unit_price(self):
        unit_price= Shop.objects.filter(product=self).order_by('-unit_price').first()
        if unit_price is None:
            return 0
        else:
            return unit_price.unit_price

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self,*args, **kwargs):
        self.class_name='product'
        super(Product,self).save(*args, **kwargs)

class Category(MarketPage):
    products=models.ManyToManyField("Product", blank=True,verbose_name=_("products"))
    def childs(self):
        return Category.objects.filter(parent=self)
  
      

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self,*args, **kwargs):
        self.class_name='category'
        super(Category,self).save(*args, **kwargs)

class Customer(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    customer=models.ForeignKey("customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=OrderStatusEnum.choices, max_length=50)
    date_ordered=models.DateTimeField(_("date_ordered"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_packed=models.DateTimeField(_("date_packed"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_shipped=models.DateTimeField(_("date_shipped"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_delivered=models.DateTimeField(_("date_delivered"),null=True,blank=True, auto_now=False, auto_now_add=False)
    shipper=models.ForeignKey("shipper", verbose_name=_("shipper"),null=True,blank=True, on_delete=models.CASCADE)
    ship_fee=models.IntegerField(_("ship_fee"),default=0)
    def sum_total(self):
        return self.lines_total()+self.ship_fee
    def lines_total(self):
        sum=0
        for line in self.orderline_set.all():
            sum+=line.total()
        return sum
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"{str(self.supplier)} / {str(self.customer)} "

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

class OrderLine(models.Model):
    order=models.ForeignKey("order", verbose_name=_("order"), on_delete=models.CASCADE)
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    unit_name=models.CharField(_("unit_name"), max_length=50)
    unit_price=models.IntegerField(_("unit_price"))
    description=models.TextField(_("description"),blank=True)

    def total(self):
        return self.unit_price*self.quantity

    class Meta:
        verbose_name = _("OrderLine")
        verbose_name_plural = _("OrderLines")

    def __str__(self):
        return str(self.order)

    def get_absolute_url(self):
        return reverse(APP_NAME+":orderLine", kwargs={"pk": self.pk})

class CartLine(models.Model):
    customer=models.ForeignKey("customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    shop=models.ForeignKey("shop", verbose_name=_("shop"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    
    class Meta:
        verbose_name = _("CartLine")
        verbose_name_plural = _("CartLines")

    def __str__(self):
        return str(self.customer)

    def get_absolute_url(self):
        return reverse(APP_NAME+":cart_line", kwargs={"pk": self.pk})

class Shop(models.Model):
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"), max_length=50)
    old_price=models.IntegerField(_("قیمت قبلی"))
    unit_price=models.IntegerField(_("قیمت فروش"))
    available=models.IntegerField(_("تعداد موجودی"),default=10)
    date_added=models.DateTimeField(_("date-added"), auto_now=False, auto_now_add=True)
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f"{self.product.title} هر {self.unit_name} : {self.unit_price} {CURRENCY}"

    def get_absolute_url(self):
        return reverse(APP_NAME+":shop", kwargs={"pk": self.pk})

class Supplier(MarketPage):
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def save(self,*args, **kwargs):
        self.class_name="supplier"
        return super(Supplier,self).save(*args, **kwargs)

class Shipper(MarketPage):
    

    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("Shippers")

    def save(self,*args, **kwargs):
        self.class_name="shipper"
        return super(Shipper,self).save(*args, **kwargs)