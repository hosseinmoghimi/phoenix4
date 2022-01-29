from core.enums import ColorEnum
from tinymce.models import HTMLField
from core.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
IMAGE_FOLDER=APP_NAME+"/img/"
from core.models import BasicPage
from django.shortcuts import reverse


class WebPage(BasicPage):
    author=models.ForeignKey("ourteam", verbose_name=_("ourteam"),null=True,blank=True, on_delete=models.CASCADE)
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(WebPage,self).save(*args, **kwargs)


class Blog(WebPage):

    

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")


    def save(self,*args, **kwargs):
        self.class_name="blog"
        return super(Blog,self).save(*args, **kwargs)



class CryptoToken(WebPage):
    rank=models.IntegerField(_("rank"),null=True,blank=True)
    road_map=models.CharField(_("roadmap"),null=True,blank=True, max_length=5000)
    symbol=models.CharField(_("symbol"),null=True,blank=True, max_length=25)
    trading_view=models.CharField(_("trading_view"),null=True,blank=True, max_length=5000)
    coin_market_cap=models.CharField(_("coin_market_cap"),null=True,blank=True, max_length=5000)
    vendor_url=models.CharField(_("vendor_url"),null=True,blank=True, max_length=5000)
    vendor_img_origin = models.ImageField(_("تصویر آیکون"),null=True,blank=True, upload_to=IMAGE_FOLDER +
                                     'Token/icon/', height_field=None, width_field=None, max_length=None)
    price=models.CharField(_("price"),null=True,blank=True, max_length=50)
    class Meta:
        verbose_name = _("CryptoToken")
        verbose_name_plural = _("CryptoTokens")

    def vendor_img(self):
        if self.vendor_img_origin:
            return MEDIA_URL+str(self.vendor_img_origin)
        else:
            return STATIC_URL+"web/icon/token.png"
    def save(self,*args, **kwargs):
        self.class_name="cryptotoken"
        return super(CryptoToken,self).save(*args, **kwargs)


class Carousel(models.Model):
    app_name=models.CharField(_("app_name"), max_length=50)
    image_banner = models.ImageField(_("تصویر اسلایدر  1333*2000 "), upload_to=IMAGE_FOLDER +
                                     'Banner/', height_field=None, width_field=None, max_length=None)
    title = models.CharField(_("عنوان"), null=True, blank=True, max_length=500)
    body = HTMLField(_("بدنه"), null=True, blank=True, max_length=2000)
    text_color = models.CharField(_("رنگ متن"), default="#fff", max_length=20)
    height=models.IntegerField(_("height"),default=350)
    priority = models.IntegerField(_("ترتیب"), default=100)
    archive = models.BooleanField(_("بایگانی شود؟"), default=False)
    tag_number = models.IntegerField(_("عدد برچسب"), default=100)
    links=models.ManyToManyField("core.link",blank=True, verbose_name=_("links"))
    tag_text = models.CharField(
        _("متن برچسب"), max_length=100, blank=True, null=True)
    class_name="carousel"
    class Meta:
        verbose_name = _("Carousel")
        verbose_name_plural = _("اسلایدر های صفحه اصلی")

    def image(self):
        return MEDIA_URL+str(self.image_banner)

    def __str__(self):
        return str(self.priority)

    def get_edit_btn(self):
        return f"""
        <a target="_blank" href="{self.get_edit_url()}" title="ویرایش اسلایدر">
        <i class="fa fa-edit text-info"></i>
        </a>
        """
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


class OurWork(WebPage):
    # status=models.CharField(_("وضعیت"),choices=OurWorkStatusEnum.choices,default=OurWorkStatusEnum.DONE, max_length=50)
    location = models.CharField(
        _('موقعیت در نقشه گوگل 400*400'), max_length=500, null=True, blank=True)
    contract_no=models.CharField(max_length=50,null=True,blank=True)
    contract_date=models.CharField(max_length=50,null=True,blank=True)
    employer=models.CharField(max_length=100,null=True,blank=True)



    def save(self,*args,**kwargs):
        self.child_class_title='کارهای انجام شده'
        self.class_name = 'ourwork'
        self.app_name = APP_NAME
        super(OurWork, self).save(*args,**kwargs)

    class Meta:
        verbose_name = _("OurWork")
        verbose_name_plural = _("پروژه های انجام شده")


class Testimonial(models.Model):
    for_home = models.BooleanField(_("نمایش در صفحه خانه"), default=False)
    image_origin = models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Testimonial/',
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    title = models.CharField(_("عنوان"), max_length=2000)
    body = models.CharField(_("متن"), max_length=2000, null=True, blank=True)
    footer = models.CharField(_("پانوشت"), max_length=200)
    priority = models.IntegerField(_("ترتیب"), default=100)
    profile = models.ForeignKey("authentication.Profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.PROTECT)
    class_name="testimonial"
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("گفته های مشتریان")
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+"web/testimonial/icon.png"
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Testimonial_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


class Feature(WebPage):
    # question=models.CharField(_("question"), max_length=50)
    def save(self):
        self.app_name = APP_NAME
        self.class_name = 'feature'
        self.child_class_title='سرویس و خدمات'
        super(Feature, self).save()

    def get_icon_tag(self):
        if self.thumbnail_origin is not None and self.thumbnail_origin:
            return f'<img src="{MEDIA_URL}{str(self.thumbnail_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'
        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i class="text-{self.color} material-icons">{self.icon_material}</i>'
        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<span class="text-{self.color} {self.icon_fa}"></span>'
        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span class="text-{self.color}">{self.icon_svg}</span>'
        return None

    def get_tag(self):
        icon = self.get_icon_tag()
        if icon and icon is not None:
            return f'<a title="{self.title}" href="{self.get_absolute_url()}">{icon}</a>'
        return None

    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("خدمات و سرویس ها")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def ourworks(self):
        return OurWork.objects.filter(parent=self)


class Award(WebPage):
    # title=models.CharField(_("عنوان"), max_length=50)    
    # image=models.ForeignKey("GalleryPhoto", verbose_name=_("تصویر"), on_delete=models.CASCADE)
    date_award=models.DateField(auto_now=False,auto_now_add=False)
    show_in_footer=models.BooleanField(_("نمایش در پایین صفحه"),default=False)
    # show_in_home=models.BooleanField(_("نمایش در صفحه خانه"),default=False)
    # priority=models.IntegerField(_("ترتیب"),default=100)
    # description=models.CharField(_("توضیحات"), max_length=5000,null=True,blank=True)

    def save(self):
        self.app_name = APP_NAME
        self.class_name='award'
        self.child_class_title=' تقدیر نامه'
        super(Award,self).save()

    

    class Meta:
        verbose_name = _("Award")
        verbose_name_plural = _("جوایز و تقدیر نامه ها")

    # def __str__(self):
    #     return self.title


class Technology(WebPage):
    # question = models.CharField(_("سوال"), max_length=200)  

    def save(self):
        self.child_class_title='تکنولوژی'
        self.class_name = 'technology'
        self.app_name = APP_NAME
        super(Technology, self).save()

    class Meta:
        verbose_name = _("Technology")
        verbose_name_plural = _("تکنولوژی")


class CountDownItem(models.Model):
    title = models.CharField(_("Title"), max_length=500, blank=True, null=True)
    pretitle = models.CharField(
        _("Pre Title"), max_length=500, blank=True, null=True)
    for_home = models.BooleanField(_("نمایش در صفحه اصلی"), default=False)
    image_origin = models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'CountDownItem/',
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    counter = models.IntegerField(_("شمارنده"), default=100)
    priority = models.IntegerField(_("ترتیب"), default=100)

    class Meta:
        verbose_name = _("CountDownItem")
        verbose_name_plural = _("شمارنده ها")

    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.title

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/coundownitem/{self.pk}/change/'


class OurTeam(models.Model):
    class_name="ourteam"
    app_name=models.CharField(_("app_name"),null=True,blank=True, max_length=50)
    profile = models.ForeignKey("authentication.Profile", verbose_name=_(
        "پروفایل"), on_delete=models.CASCADE)
    job = models.CharField(_("سمت"), max_length=100)
    description = HTMLField(_("توضیحات"),null=True,blank=True, max_length=50000)
    priority = models.IntegerField(_("ترتیب"), default=1000)
    social_links = models.ManyToManyField(
        "core.SocialLink", verbose_name=_("social_links"), blank=True)
    
    for_home=models.BooleanField(_("for_home"),default=False)
    def __str__(self):
        return self.profile.name

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'OurTeam'
        managed = True
        verbose_name = 'OurTeam'
        verbose_name_plural = 'تیم ما'

    def get_absolute_url(self):
        return reverse(APP_NAME+":ourteam",kwargs={'pk':self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
class ContactMessage(models.Model):
    full_name = models.CharField(_("نام کامل"), max_length=50)
    mobile = models.CharField(_("شماره تماس"), max_length=50)
    email = models.EmailField(_("ایمیل"), max_length=254)
    subject = models.CharField(_("عنوان پیام"), max_length=50)
    message = models.CharField(_("متن پیام"), max_length=50)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    app_name = models.CharField(_("اپلیکیشن"), max_length=50)

    class Meta:
        verbose_name = _("ContactMessage")
        verbose_name_plural = _("پیام های ارتباط با ما")

    def __str__(self):
        return self.full_name


class FAQ(models.Model):
    for_home = models.BooleanField(_("نمایش در صفحه خانه"), default=False)
    color = models.CharField(
        _("رنگ"), choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)

    # icon = models.ForeignKey(
    #     "core.icon", null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.IntegerField(_("ترتیب"))
    question = models.CharField(_("سوال"), max_length=200)
    answer = models.CharField(_("پاسخ"), max_length=5000)
    class_name='faq'

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("پرسش های متداول")

    def __str__(self):
        return self.question

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

    def get_absolute_url(self):
        return reverse("web:faq")

