from datetime import timezone
from .apps import APP_NAME
from .constants import *
from .enums import *
# from app.repo import ParameterRepo
from core import models as CoreModels
from .enums import *
from .constants import *
from .settings import *
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from tinymce import models as tinymce_models
from utility.persian import PersianCalendar
IMAGE_FOLDER = APP_NAME+'/images/'


class LiveStockPage(CoreModels.BasicPage):

    class Meta:
        verbose_name = _("LiveStockPage")
        verbose_name_plural = _("LiveStockPages")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(LiveStockPage, self).save(*args, **kwargs)


class Log(models.Model):
    title = models.CharField(_("title"), max_length=50)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)

    animal = models.ForeignKey("animal", verbose_name=_(
        "animal"), null=True, blank=True, on_delete=models.CASCADE)
    employee = models.ForeignKey("employee", verbose_name=_(
        "employee"), null=True, blank=True, on_delete=models.CASCADE)
    saloon = models.ForeignKey("saloon", verbose_name=_(
        "saloon"), null=True, blank=True, on_delete=models.CASCADE)
    farm = models.ForeignKey("farm", verbose_name=_(
        "farm"), null=True, blank=True, on_delete=models.CASCADE)

    description = models.CharField(
        _("description"), null=True, blank=True, max_length=500)

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Log_detail", kwargs={"pk": self.pk})


class AnimalInSaloon(models.Model):
    animal = models.ForeignKey(
        "animal", verbose_name='animal', on_delete=models.CASCADE)
    saloon = models.ForeignKey(
        "saloon", verbose_name='saloon', on_delete=models.CASCADE)
    animal_price = models.IntegerField(_("price"), default=0)
    enter_date = models.DateTimeField(
        _("تاریخ ورود"), auto_now=False, auto_now_add=False)
    exit_date = models.DateTimeField(
        _("تاریخ خروج"), null=True, blank=True, auto_now=False, auto_now_add=False)
    animal_weight=models.FloatField(_("weight"),default=0)
    class_name = "animalinsaloon"
    employee=models.ForeignKey("employee",null=True,blank=True, verbose_name=_("employee"), on_delete=models.CASCADE)
    def __str__(self):
        return f"""{self.animal.name} -> {self.saloon.name}"""

    class Meta:
        verbose_name = 'AnimalInSaloon'
        verbose_name_plural = 'AnimalInSaloons'

    def persian_enter_date(self):
        return PersianCalendar().from_gregorian(self.enter_date)

    def persian_exit_date(self):
        if self.exit_date is None:
            return ""
        return PersianCalendar().from_gregorian(self.exit_date)

    def get_edit_url(self):
        return f"{CoreSettings.ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

    def get_edit_btn(self):
        return f"""
            <a title="ویرایش" href="{self.get_edit_url()}">
                <span class="material-icons">
                    edit
                </sapn>
            </a>
        """


class Animal(models.Model):
    name = models.CharField(_("name"), max_length=50)
    category = models.CharField(
        _("category"), choices=AnimalCategoryEnum.choices, max_length=50)
    tag = models.CharField(_("tag"), default='0000', max_length=50)
    class_name = 'animal'
    image_origin = models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"animal/",
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    # current_saloon=models.ForeignKey("saloon", verbose_name=_("saloon"),null=True,blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("Animal")
        verbose_name_plural = _("Animals")

    def image(self):
        im = ""
        if self.image_origin:
            return CoreSettings.MEDIA_URL+str(self.image_origin)
        elif self.category == AnimalCategoryEnum.COW:
            im = 'cow.jpg'
        elif self.category == AnimalCategoryEnum.COW:
            im = 'cow.jpg'
        elif self.category == AnimalCategoryEnum.SHEEP:
            im = 'sheep.jpg'
        elif self.category == AnimalCategoryEnum.OSTRICH:
            im = 'ostrich.jpg'
        elif self.category == AnimalCategoryEnum.CHICKEN:
            im = 'chicken.jpg'
        elif self.category == AnimalCategoryEnum.TURKEY:
            im = 'turkey.jpg'
        return f'{CoreSettings.STATIC_URL}{APP_NAME}/img/animal/{im}'

    def __str__(self):
        return self.name+" " + self.tag

    def current_in_saloon(self, report_date=None):
        aa = AnimalInSaloon.objects.filter(animal=self).order_by('-enter_date')
        if report_date is None:
            from django.utils import timezone as tz
            report_date = tz.now()
        aa = aa.filter(enter_date__lte=report_date)
        # aa = aa.filter(models.Q(exit_date=None) |
        #                models.Q(exit_date__gte=report_date))
        aa = aa.first()
        return aa

    def get_absolute_url(self):
        return reverse(APP_NAME+":animal", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{CoreSettings.ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

    def get_edit_btn(self):
        return f"""
            <a title="ویرایش" href="{self.get_edit_url()}">
                <span class="material-icons">
                    edit
                </sapn>
            </a>
        """

    def foods(self, *args, **kwargs):
        foods = []
        animal_in_saloons = self.animalinsaloon_set.all()
        for animal_in_saloon in animal_in_saloons:
            saloonfood_set = animal_in_saloon.saloon.saloonfood_set.filter(
                food_date__gte=animal_in_saloon.enter_date)
            if animal_in_saloon.exit_date is not None:
                saloonfood_set = saloonfood_set.filter(
                    food_date__lte=animal_in_saloon.exit_date)
            for saloon_food in saloonfood_set:
                foods.append(saloon_food)
        return foods
    def price(self):
        price=0
        try:
            a=AnimalInSaloon.objects.filter(animal=self).order_by("-enter_date").first()
            if a is not None:
                price= a.animal_price
        except:
            pass    
        return price

class Employee(models.Model):
    profile = models.ForeignKey("authentication.profile", related_name="farm_employee_set", verbose_name=_(
        "profile"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return self.profile.name()

    def get_absolute_url(self):
        return reverse(APP_NAME+":employee", kwargs={"pk": self.pk})


class Saloon(models.Model):
    farm = models.ForeignKey("farm", verbose_name=_(
        "farm"), on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("Saloon")
        verbose_name_plural = _("Saloons")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":saloon", kwargs={"pk": self.pk})
    def sum_animal_price(self):
        sum1=0
        for animal in Animal.objects.all():
            sum1+=animal.price()
        return sum1


class Farm(models.Model):
    name = models.CharField(_("name"), max_length=50)
    class_name = 'farm'
    app_name = APP_NAME

    class Meta:
        verbose_name = _("Farm")
        verbose_name_plural = _("Farms")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":farm", kwargs={"pk": self.pk})


class Doctor(models.Model):
    profile = models.ForeignKey("authentication.profile", related_name="farm_doctor_set", verbose_name=_(
        "profile"), on_delete=models.CASCADE)

    class_name = 'farm'
    app_name = APP_NAME

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")

    def __str__(self):
        return self.profile.name()

    def get_absolute_url(self):
        return reverse(APP_NAME+":doctor", kwargs={"pk": self.pk})


class Drug(LiveStockPage):

    class Meta:
        verbose_name = _("Drug")
        verbose_name_plural = _("Drugs")

    def save(self, *args, **kwargs):
        self.child_class = "drug"
        return super(Drug, self).save(*args, **kwargs)


class Food(LiveStockPage):
    unit_name = models.CharField(
        _("unit_name"), choices=CoreEnums.UnitNameEnum.choices, default=CoreEnums.UnitNameEnum.KILOGERAM, max_length=50)
    unit_price = models.IntegerField(_("unit_price"), default=1000)

    app_name=APP_NAME
    class_name="food"
    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")

    def save(self, *args, **kwargs):
        self.child_class = "food"
        return super(Food, self).save(*args, **kwargs)


class SaloonFood(models.Model):
    saloon = models.ForeignKey("saloon", verbose_name=_(
        "saloon"), on_delete=models.CASCADE)
    food = models.ForeignKey("food", verbose_name=_(
        "food"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("quantity"))
    unit_name = models.CharField(
        _("unit_name"), choices=CoreEnums.UnitNameEnum.choices, max_length=50)
    unit_price = models.IntegerField(_("قیمت واحد"))
    food_date = models.DateTimeField(
        _("food_date"), auto_now=False, auto_now_add=False)
    employee=models.ForeignKey("employee",null=True,blank=True, verbose_name=_("employee"), on_delete=models.CASCADE)
    
    class_name="saloonfood"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("SaloonFood")
        verbose_name_plural = _("SaloonFoods")

    def total_line(self):
        return self.unit_price*self.quantity

    def __str__(self):
        return f'{self.saloon} {self.food} {self.quantity}  {self.unit_name} {PersianCalendar().from_gregorian(self.food_date)}'

    def get_absolute_url(self):
        return reverse(APP_NAME+":saloonfood", kwargs={"pk": self.pk})

    def food_per_animal(self):
        from .repo import SaloonRepo
        population = len(SaloonRepo().animals_in_saloon(
            saloon=self.saloon, report_date=self.food_date))
        if population == 0:
            quantity = 0
        else:
            quantity = self.quantity/population
        return {
            'quantity': quantity,
            'total': quantity*self.unit_price,
        }
    def get_edit_url(self):
        return f"{CoreSettings.ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

    def get_edit_btn(self):
        return f"""
            <a title="ویرایش" href="{self.get_edit_url()}">
                <span class="material-icons">
                    edit
                </sapn>
            </a>
        """