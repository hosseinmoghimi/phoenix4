from django.db import models
from core.models import BasicPage
from .apps import APP_NAME
from django.utils.translation import gettext as _
from django.shortcuts import reverse



class MarketPage(BasicPage):

    

    class Meta:
        verbose_name = _("MarketPage")
        verbose_name_plural = _("MarketPages")

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        super(MarketPage,self).save(*args, **kwargs)

        
class Product(MarketPage):

    

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