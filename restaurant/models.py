from django.db import models
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.settings import ADMIN_URL
from utility.persian import PersianCalendar
from restaurant.enums import MealTypeEnum
from .apps import APP_NAME
from core.models import BasicPage as CoreBasicPage
class RestaurantPage(CoreBasicPage):

    
    class Meta:
        verbose_name = _("TaxPage")
        verbose_name_plural = _("TaxPages")

    def save(self, *args, **kwargs):
        self.app_name = APP_NAME
        return super(RestaurantPage, self).save(*args, **kwargs)



class Guest(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    
    class_name="guest"
    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")

    def __str__(self):
        return self.profile.name
 

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

class Food(RestaurantPage):

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")

      
    def save(self, *args, **kwargs):
        self.class_name = 'food'
        return super(Food, self).save(*args, **kwargs)


class Meal(models.Model):
    food=models.ForeignKey("food", verbose_name=_("food"), on_delete=models.CASCADE)
    date_served=models.DateField(_("date_served"), auto_now=False, auto_now_add=False)
    meal_type=models.CharField(_("meal type"),choices=MealTypeEnum.choices, max_length=50)
    reserved=models.BooleanField(_("reserved"),default=False)
    def is_reserved(self, *args, **kwargs):
        if 'guest_id' not in kwargs:
            return False
        guest_id=kwargs['guest_id']
        self.reserved= len(self.reservedmeal_set.filter(guest_id=guest_id))>0
        return self.reserved

    class_name="meal"
    def reserves_count(self):
        return len(self.reservedmeal_set.all())
    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{str(self.food)} # {self.meal_type} @ {self.persian_date_served()}"

    def get_absolute_url(self):
        return reverse(APP_NAME+":meal", kwargs={"pk": self.pk})

    def persian_date_served(self):
        return PersianCalendar().from_gregorian(self.date_served)[:10]


    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"


class ReservedMeal(models.Model):
    guest=models.ForeignKey("guest", verbose_name=_("guest"), on_delete=models.CASCADE)
    meal=models.ForeignKey("meal", verbose_name=_("meal"), on_delete=models.CASCADE)
    date_reserved=models.DateTimeField(_("date_reserved"), auto_now=False, auto_now_add=True)
    date_served=models.DateTimeField(_("date_served"),null=True,blank=True, auto_now=False, auto_now_add=False)
    class_name="reservedmeal"

    class Meta:
        verbose_name = _("ReservedMeal")
        verbose_name_plural = _("ReservedMeals")

    def persian_date_reserved(self):
        return PersianCalendar().from_gregorian(self.date_reserved)


    def __str__(self):
        return f"""{("***" if self.date_served is not None else "")} {str(self.guest)} {str(self.meal)}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

        
    def persian_date_served(self):
        return PersianCalendar().from_gregorian(self.date_served)


class Host(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    
    class_name="host"
    class Meta:
        verbose_name = _("Host")
        verbose_name_plural = _("Hosts")

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
 