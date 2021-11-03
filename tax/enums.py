from core.enums import *
from django.utils.translation import gettext as _

class TaxStatusEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار")
 

def StatusColor(status):
    color="primary"
    if status==TaxStatusEnum.IMPORT:
        color= 'primary'
    elif status==TaxStatusEnum.EXPORT:
        color= 'warning'
    return color