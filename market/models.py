from django.db.models.base import Model
from django.db.models.fields.reverse_related import ManyToOneRel
from utility.persian2 import PersianCalendar
from utility.qrcode import generate_qrcode
from core.settings import ADMIN_URL, MEDIA_URL,QRCODE_ROOT,QRCODE_URL,SITE_FULL_BASE_ADDRESS, STATIC_URL
from django.db.models.fields import CharField
from market.enums import DegreeLevelEnum, EmployeeEnum, OrderLineStatusEnum, OrderStatusEnum, ShopLevelEnum
from django.db import models
from core.models import BasicPage
from .apps import APP_NAME
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.constants import CURRENCY
from utility.currency import to_price

IMAGE_FOLDER=APP_NAME+"/imags/"

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
    brand=models.ForeignKey("brand",null=True,blank=True, verbose_name=_("brand"),on_delete=models.CASCADE)
    model_name=models.CharField(_("model"),null=True,blank=True, max_length=50)
    unit_names=models.ManyToManyField("unitname", verbose_name=_("unit_names"))
    for_category=models.BooleanField(_("نمایش در صفحه دسته بندی"))
    def old_price(self):
        old_price= Shop.objects.filter(product=self).order_by('-old_price').first()
        if old_price is None:
            return None
        if old_price.old_price==0:
            return None
        
        return old_price.old_price
    def unit_price(self):
        unit_price= Shop.objects.filter(product=self).order_by('-unit_price').first()
        if unit_price is None:
            return None
            
        else:
            return unit_price.unit_price

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def save(self,*args, **kwargs):
        self.class_name='product'
        super(Product,self).save(*args, **kwargs)
    def category(self):
        return self.category_set.first()

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

class ShopRegion(models.Model):
    name=models.CharField(_("name"), max_length=50)

    

    class Meta:
        verbose_name = _("ShopRegion")
        verbose_name_plural = _("ShopRegions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ShopRegion_detail", kwargs={"pk": self.pk})

class Customer(models.Model):
    title=models.CharField(_("title"), max_length=50)
    region=models.ForeignKey("shopregion",verbose_name=_("shop_region"), on_delete=models.CASCADE)
    level=models.CharField(_("level"),choices=ShopLevelEnum.choices,default=ShopLevelEnum.REGULAR, max_length=50)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    def cart(self):
        return Cart.objects.filter(customer=self).first()
    def get_orders_url(self):
        return reverse(APP_NAME+":orders",
            kwargs={
                'customer_id':self.pk,
                'supplier_id':0,
                'shipper_id':0
            })

    def get_cart_url(self):
        return reverse(APP_NAME+":customer_cart",kwargs={'customer_id':self.customer.id})

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":customer", kwargs={"pk": self.pk})

class Order(models.Model):
    customer=models.ForeignKey("customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=OrderStatusEnum.choices, max_length=50)
    count_of_packs=models.IntegerField(_("تعداد پاکت"),default=1)
    date_ordered=models.DateTimeField(_("date_ordered"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_accepted=models.DateTimeField(_("date_accepted"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_packed=models.DateTimeField(_("date_packed"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_shipped=models.DateTimeField(_("date_shipped"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_cancelled=models.DateTimeField(_("date_cancelled"),null=True,blank=True, auto_now=False, auto_now_add=False)
    date_delivered=models.DateTimeField(_("date_delivered"),null=True,blank=True, auto_now=False, auto_now_add=False)
    shipper=models.ForeignKey("shipper", verbose_name=_("shipper"),null=True,blank=True, on_delete=models.CASCADE)
    ship_fee=models.IntegerField(_("ship_fee"),default=0)
    description=models.CharField(_("description"),max_length=500,null=True,blank=True)
    address=models.CharField(_("description"),max_length=500,null=True,blank=True)
    no_ship=models.BooleanField(_("خود مشتری مراجعه و تحویل میگیرد؟"))
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
    def total(self):
        return self.lines_total()+self.ship_fee
    def __str__(self):
        return f"سفارش شماره {str(self.pk)} /{str(self.supplier)} / {str(self.customer)} "

    def get_absolute_url(self):
        return reverse(APP_NAME+":order", kwargs={"pk": self.pk})

    def get_invoice_url(self):
        return reverse(APP_NAME+":order_invoice", kwargs={"pk": self.pk})
    def get_status_color(self):
        status_color='primary'
        if self.status==OrderStatusEnum.ACCEPTED:
            status_color='info'
        if self.status==OrderStatusEnum.CANCELED:
            status_color='secondary'
        if self.status==OrderStatusEnum.CONFIRMED:
            status_color='success'
        if self.status==OrderStatusEnum.SHIPPED:
            status_color='warning'
        if self.status==OrderStatusEnum.PACKING:
            status_color='danger'
        if self.status==OrderStatusEnum.PACKED:
            status_color='success'
        if self.status==OrderStatusEnum.DELIVERED:
            status_color='dark'
        return status_color
    def get_status_tag(self):
        status_color=self.get_status_color()
        return f"""
        <span class="badge badge-{status_color}">{self.status}</span>
        """
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+"/order/"+str(self.pk)+"/change/"
class OrderLine(models.Model):
    order=models.ForeignKey("order", verbose_name=_("order"), on_delete=models.CASCADE)
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    unit_name=models.CharField(_("unit_name"), max_length=50)
    unit_price=models.IntegerField(_("unit_price"))
    description=models.TextField(_("description"),blank=True)
    status=models.CharField(_("status"),choices=OrderLineStatusEnum.choices,default=OrderLineStatusEnum.CART, max_length=50)

    def guarantees(self):
        return Guarantee.objects.filter(orderline=self)

    def total(self):
        return self.unit_price*self.quantity

    class Meta:
        verbose_name = _("OrderLine")
        verbose_name_plural = _("OrderLines")

    def __str__(self):
        return f"{str(self.order)} : {self.product.title} : {self.quantity} {self.unit_name} {to_price(self.unit_price)}ی/ {to_price(self.unit_price*self.quantity)}"

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
        return f"{str(self.customer)} : {self.quantity} {self.shop.unit_name} {self.shop.product.title} از {self.shop.supplier.title}"

    def get_absolute_url(self):
        return reverse(APP_NAME+":cart_line", kwargs={"pk": self.pk})
    def line_total(self):
        return self.shop.unit_price*self.quantity

class Offer(MarketPage):
    shops=models.ManyToManyField("shop", verbose_name=_("shops"))
    col=models.IntegerField(_("col"),default=4)
    

    class Meta:
        verbose_name = _("Offer")
        verbose_name_plural = _("Offers")

    def save(self,*args, **kwargs):
        self.class_name='offer'
        super(Offer,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(APP_NAME+":offer", kwargs={"pk": self.pk})

class Blog(MarketPage):

    

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")


    def save(self,*args, **kwargs):
        self.class_name="blog"
        return super(Blog,self).save(*args, **kwargs)

class Shop(models.Model):
    level=models.CharField(_("level"),choices=ShopLevelEnum.choices,default=ShopLevelEnum.REGULAR, max_length=50)
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"), max_length=50)
    old_price=models.IntegerField(_("قیمت قبلی"),default=0)
    unit_price=models.IntegerField(_("قیمت فروش"))
    available=models.IntegerField(_("تعداد موجودی"),default=10)
    date_added=models.DateTimeField(_("date-added"), auto_now=False, auto_now_add=True)
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f"{self.product.title} برای {self.level} هر {self.unit_name} : {self.unit_price} {CURRENCY} فروش توسط {self.supplier.title}"

    def get_absolute_url(self):
        return reverse(APP_NAME+":shop", kwargs={"pk": self.pk})

class Supplier(MarketPage):

    region=models.ForeignKey("shopregion", verbose_name=_("shop_region"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    ship_fee=models.IntegerField(_("ship_fee"),default=0)
    logo_origin=models.ImageField(_("logo"), null=True,blank=True,upload_to=IMAGE_FOLDER+"suppier/logo/", height_field=None, width_field=None, max_length=None)
    warehouses=models.ManyToManyField("market.WareHouse", verbose_name=_("warehouses"),blank=True)
    employees=models.ManyToManyField("Employee", verbose_name=_("کارکنان"),blank=True)
    def logo(self):
        if self.logo_origin:
            return f"{MEDIA_URL}{self.logo_origin}"
        return f"{STATIC_URL}{APP_NAME}/img/pages/thumbnail/supplier-logo.png"
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def save(self,*args, **kwargs):
        self.class_name="supplier"
        return super(Supplier,self).save(*args, **kwargs)

class Shipper(MarketPage):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("Shippers")

    def save(self,*args, **kwargs):
        self.class_name="shipper"
        return super(Shipper,self).save(*args, **kwargs)

class WareHouse(models.Model):
    name=models.CharField(_("نام انبار"), max_length=50)
    address=models.CharField(_("آدرس"), max_length=100)
    employees=models.ManyToManyField("Employee", verbose_name=_("کارکنان"),blank=True)
    def products_in_stock(self):
        products_in_stock=[]
        for orderinwarehouse in self.orderinwarehouse_set.all():
            for line in orderinwarehouse.order.orderline_set.all():

                if not line.product in (p.product for p in products_in_stock):
                    product_in_stock=ProductInStock(unit_name="",product=line.product,description="",adder=orderinwarehouse.adder,ware_house=self,quantity=0,date_added=orderinwarehouse.date_added)
                    products_in_stock.append(product_in_stock)
        return products_in_stock
    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("انبار های کالا")

    def __str__(self):
        return self.name

        

    def get_absolute_url(self):
        return reverse(APP_NAME+":ware_house", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/warehouse/{self.pk}/change/'

class Guarantee(models.Model):
    orderline=models.ForeignKey("OrderLine", verbose_name=_("سفارش"), on_delete=models.CASCADE)
    barcode=models.CharField(_("بارکد"), max_length=50,null=True,blank=True)
    serial_no=models.CharField(_("شماره سریال"), max_length=50,null=True,blank=True)
    start_date=models.DateTimeField(_("شروع گارانتی"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("اتمام گارانتی"), auto_now=False, auto_now_add=False)
    class_name="guarantee"

    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/guarantee/{self.pk}/change/'
    def get_qrcode_url(self):
        
        file_name=self.class_name+str(self.pk)+".svg"       
        return f"{QRCODE_URL}{file_name}"

    def generate_qrcode(self):
        if self.pk is None:
            super(Guarantee,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        # file_address=os.path.join(file_path,file_name)
        file_address=os.path.join(QRCODE_ROOT,file_name)
   
        content=SITE_FULL_BASE_ADDRESS+self.get_absolute_url()
        generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
    def save(self):

        self.generate_qrcode()
        super(Guarantee,self).save()

    class Meta:
        verbose_name = _("Guarantee")
        verbose_name_plural = _("خدمات پس از فروش و گارانتی")

    def __str__(self):
        return self.barcode

    def get_absolute_url(self):
        return reverse(APP_NAME+":guarantee", kwargs={"pk": self.pk})

class Brand(models.Model):
    prefix=models.CharField(_("پیش تعریف"), max_length=200,default='',null=True,blank=True)
    title=models.CharField(_("نام برند"), max_length=50)
    description=models.CharField(_("توضیحات"), max_length=500,default='',null=True,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Brand/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    header_image_origin=models.ImageField(_("تصویر سربرگ"), upload_to=IMAGE_FOLDER+'Brand/Header/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    rate=models.IntegerField(_("امتیاز"),default=0)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    url=models.CharField(_("آدرس اینترتی"),null=True,blank=True,max_length=100)
    persian_title=models.CharField(_("نام فارسی"),null=True,blank=True, max_length=50)
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        else:
            return STATIC_URL+"market/img/pages/image/brand.png"

    def header_image(self):
        return MEDIA_URL+str(self.header_image_origin)
    def get_edit_btn(self):
        return f"""
        <a class="text-info google-drive-opener" href="{self.get_edit_url()}">
            <i class="material-icons" aria-hidden="true">settings</i>
            ویرایش 
            </a>
        """

    def get_logo_link(self):
        return f"""
         <a title="{self.title}" target="_blank"
            href="{self.get_absolute_url()}">
            <img src="{self.image()}" height="64" alt="{self.title}">

        </a>
        """
    class Meta:
        verbose_name = _("برند")
        verbose_name_plural = _("برند ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("market:brand", kwargs={"pk": self.pk})
        # return self.url
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/brand/'+str(self.pk)+'/change/'
  

class Cart(models.Model):
    lines=[]
    customer=models.ForeignKey("customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    # lines=models.ManyToManyField("cartline",blank=True, verbose_name=_("lines"))
    # def orders(self):
    #     return CartLine.objects.filter(customer=self.customer)
    # def lines(self):
    #     return OrderLine.objects.filter(customer=self.customer)
    orders=[]
    

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return self.customer.profile.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":customer_cart", kwargs={"customer_id": self.pk})



class ProductInStock(models.Model):
    adder=models.ForeignKey("Employee",null=True,blank=True, verbose_name=_("ثبت کننده"), on_delete=models.PROTECT)
    ware_house=models.ForeignKey("WareHouse", verbose_name=_("انبار"), on_delete=models.PROTECT)
    product=models.ForeignKey("Product", verbose_name=_("کالا"), on_delete=models.PROTECT)
    quantity=models.IntegerField(_("تعداد"))
    unit_name=models.CharField(_("واحد"),max_length=50)
    date_added=models.DateTimeField(_("تاریخ ثبت"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("توضیحات"), max_length=500,null=True,blank=True)
    def lines(self):
        lines=[]
        orderinwarehouses=self.ware_house.orderinwarehouse_set.all()
        for orderinwarehouse in orderinwarehouses:
            for line in orderinwarehouse.order.orderline_set.all():
                if line.product==self.product:
                    lines.append({'direction':orderinwarehouse.direction,'order':orderinwarehouse.order,'quantity':line.quantity,'unit_name':line.unit_name})
        return lines
    @property
    def available(self):
        available=0
        for line in self.lines():
            if line['direction']:
                available+=line['quantity']
            else:
                available-=line['quantity']
        return available
        
    class Meta:
        verbose_name = _("ProductInStock")
        verbose_name_plural = _("کالاهای موجود در انبار")

    def __str__(self):
        return f'{self.ware_house.name} => {self.product.title} : {self.quantity} {self.unit_name} ({self.available})'

    def get_absolute_url(self):
        return reverse(APP_NAME+":product_in_stock", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/productinstock/{self.pk}/change/'

class ProductFeature(MarketPage):
    # product=models.ForeignKey("Product",related_name="productfeature_sett", verbose_name=_("product"), on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("ProductFeature")
        verbose_name_plural = _("فیچر های کالا ها و محصولات")


    def save(self,*args, **kwargs):
        self.child_class='productfeature'
        super(ProductFeature,self).save(*args, **kwargs)
   

class Employee(models.Model):

    
    profile = models.ForeignKey("authentication.Profile", related_name='profile_employees', verbose_name=_(
        "profile"), null=True, blank=True, on_delete=models.PROTECT)
    
    role = models.CharField(_("نقش"), choices=EmployeeEnum.choices,
                            default=EmployeeEnum.DEFAULT, max_length=50)
    degree = models.CharField(_("مدرک"), choices=DegreeLevelEnum.choices,
                              default=DegreeLevelEnum.KARSHENASI, max_length=50)
    major = models.CharField(
        _("رشته تحصیلی"), null=True, blank=True, max_length=50)
    
    def __str__(self):
        return f"""{self.profile.name} {self.role}"""

    def get_link(self):
        return f"""<a href="{self.get_absolute_url()}">
                <i class="fa fa-user"></i>
                {self.profile.name()}
            </a>"""

    
    def save(self):
        return super(Employee, self).save()
    def image(self):
        return self.profile.image()
    def name(self):
        if self.profile is not None:
            return f'{self.profile.name()}'
        return '_'

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees - کارکنان")

    def get_absolute_url(self):
        return reverse(APP_NAME+':employee',kwargs={'pk':self.pk})

    def get_edit_url(self):
        if self.profile is not None:
            return self.profile.get_edit_url()



class OrderInWareHouse(models.Model):
    direction=models.BooleanField(_("ورود به انبار ؟"),default=True)
    adder=models.ForeignKey("Employee",null=True,blank=True, verbose_name=_("ثبت کننده"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    order=models.ForeignKey("Order", verbose_name=_("سفارش"), on_delete=models.CASCADE)
    ware_house=models.ForeignKey("warehouse", verbose_name=_("انبار"), on_delete=models.CASCADE)
    description=models.CharField(_("توضیحات"),null=True,blank=True, max_length=50)
    
    class Meta:
        verbose_name = _("ثبت سفارش در دفتر انبار")
        verbose_name_plural = _("OrderInWareHouses")

    def __str__(self):
        return f"""سفارش شماره {self.order.id} {("ورود به" if self.direction else "خروج از")} {self.ware_house.name}"""
    def save(self,*args, **kwargs):
        list1=OrderInWareHouse.objects.filter(order=self.order).filter(direction=self.direction)
        if not len(list1)==1:
            return super(OrderInWareHouse,self).save(*args, **kwargs)
        else:
            list1.delete()
            return super(OrderInWareHouse,self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("OrderInWareHouse_detail", kwargs={"pk": self.pk})
