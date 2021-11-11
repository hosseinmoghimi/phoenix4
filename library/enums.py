from core.enums import *
from django.utils.translation import gettext as _

class BlogStatusEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار")
 

def StatusColor(status):
    color="primary"
    if status==BlogStatusEnum.IMPORT:
        color= 'primary'
    elif status==BlogStatusEnum.EXPORT:
        color= 'warning'
    return color
class MemberShipLevelEnum(TextChoices):
    REGULAR="عادی",_("عادی")
    MASTER="استاد",_("استاد")