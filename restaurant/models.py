from django.db import models
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext as _
from django.shortcuts import reverse
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
    

    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse("Member_detail", kwargs={"pk": self.pk})



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

    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{str(self.food)} # {self.meal_type} @ {self.persian_date_served()}"

    def get_absolute_url(self):
        return reverse("Meal_detail", kwargs={"pk": self.pk})

    def persian_date_served(self):
        return PersianCalendar().from_gregorian(self.date_served)[:10]


class ReservedMeal(models.Model):
    guest=models.ForeignKey("guest", verbose_name=_("guest"), on_delete=models.CASCADE)
    meal=models.ForeignKey("meal", verbose_name=_("meal"), on_delete=models.CASCADE)
    date_reserved=models.DateTimeField(_("date_reserved"), auto_now=False, auto_now_add=False)
    date_served=models.DateTimeField(_("date_served"),null=True,blank=True, auto_now=False, auto_now_add=False)
    

    class Meta:
        verbose_name = _("ReservedMeal")
        verbose_name_plural = _("ReservedMeals")

    def __str__(self):
        return f"{str(self.guest)} {str(self.meal)}"

    def get_absolute_url(self):
        return reverse("ReservedMeal_detail", kwargs={"pk": self.pk})
