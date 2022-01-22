from django.db import models
from django.utils.translation import gettext as _
from .apps import APP_NAME
from core.models import BasicPage
from django.shortcuts import reverse

class CryptoPage(BasicPage):

    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(CryptoPage,self).save(*args, **kwargs)


class CryptoToken(CryptoPage):

    

    class Meta:
        verbose_name = _("CryptoToken")
        verbose_name_plural = _("CryptoTokens")
 
    def save(self,*args, **kwargs):
        self.class_name="food"
        return super(CryptoToken,self).save(*args, **kwargs)
