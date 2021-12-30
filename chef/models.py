from django.db import models
from django.utils.translation import gettext as _
from .apps import APP_NAME
from core.models import BasicPage
from django.shortcuts import reverse

class ChefPage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        print(200*"#")
        print("APP_NAME")
        print(APP_NAME)
        return super(ChefPage,self).save(*args, **kwargs)


class Food(ChefPage):

    

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")
 
    def save(self,*args, **kwargs):
        self.class_name="food"
        return super(Food,self).save(*args, **kwargs)
  