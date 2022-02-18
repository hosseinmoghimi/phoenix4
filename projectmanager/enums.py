from core.enums import *
from django.utils.translation import gettext as _

class WareHouseSheetDirectionEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار")


class RequestTypeEnum(TextChoices):
    MATERIAL_REQUEST='درخواست متریال',_('درخواست متریال')
    SERVICE_REQUEST='درخواست سرویس',_('درخواست سرویس')

class SignatureStatusEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال بررسی',_('درحال بررسی')
    DENIED='رد شده',_('ردشده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    PURCHASING='درحال خرید',_('درحال خرید')
    REQUESTED='درخواست شده',_('درخواست شده')
    PAID='تسویه شده',_('تسویه شده')


class ProjectStatusEnum(TextChoices):
    INITIAL='تعریف اولیه',_('تعریف اولیه')
    DRAFT='پیش نویس',_('پیش نویس')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال اجرا',_('درحال اجرا')
    DENIED='رد شده',_('ردشده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    REQUESTED='درخواست شده',_('درخواست شده')
    CANCELED='کنسل شده',_('کنسل شده')
    PAID='تسویه شده',_('تسویه شده')

class RequestStatusEnum(TextChoices):

    DEFAULT='DEFAULT',_('DEFAULT')
    INITIAL='تعریف اولیه در سیستم',_('تعریف اولیه در سیستم')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال انجام',_('در حال انجام')
    DENIED='رد شده',_('رد شده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    REQUESTED='درخواست شده',_('درخواست شده')
    PURCHASING='در حال خرید',_('در حال خرید')
    EMPLOYERS='متعلق به کارفرما',_('متعلق به کارفرما')
    AVAILABLE_IN_STORE="موجود در انبار",_("موجود در انبار")
    EXPORT_FROM_WARE_HOUSE="خارج شده از انبار",_("خارج شده از انبار")
    IMPORT_TO_WARE_HOUSE="وارد شده به انبار",_("وارد شده به انبار")

class AssignmentStatusEnum(TextChoices):
    DEFAULT='تعریف اولیه',_('تعریف اولیه')
    IN_PROGRESS='در جریان',_('در جریان')
    DONE='انجام شده',_('انجام شده')
    STOPEED='متوقف شده',_('متوقف شده')
    DENIED='رد شده',_('رد شده')
    INITIAL='ابلاغ شده',_('ابلاغ شده')
        

def StatusColor(status):
    color="primary"
    if status==ProjectStatusEnum.INITIAL:
        color= 'primary'
    elif status==ProjectStatusEnum.IN_PROGRESS:
        color= 'warning'
    elif status==ProjectStatusEnum.DENIED:
        color= 'danger'
    elif status==ProjectStatusEnum.DELIVERED:
        color= 'success'
    elif status==ProjectStatusEnum.ACCEPTED:
        color= 'success'
    elif status==ProjectStatusEnum.REQUESTED:
        color= 'primary'
    elif status==ProjectStatusEnum.CANCELED:
        color= 'secondary'
    elif status==AssignmentStatusEnum.DEFAULT:
        color= 'rose'
    elif status==AssignmentStatusEnum.IN_PROGRESS:
        color= 'info'
    elif status==AssignmentStatusEnum.DONE:
        color= 'success'
    elif status==AssignmentStatusEnum.STOPEED:
        color= 'secondary'
    elif status==AssignmentStatusEnum.DENIED:
        color= 'danger'
    elif status==RequestStatusEnum.DEFAULT:
        color= 'rose'
    elif status==RequestStatusEnum.AVAILABLE_IN_STORE:
        color= 'success'
    elif status==RequestStatusEnum.EMPLOYERS:
        color= 'info'
    elif status==RequestStatusEnum.IN_PROGRESS:
        color= 'info'
    elif status==RequestStatusEnum.ACCEPTED:
        color= 'success'
    elif status==RequestStatusEnum.DELIVERED:
        color= 'success'
    elif status==RequestStatusEnum.DENIED:
        color= 'danger'
    elif status==RequestStatusEnum.PURCHASING:
        color= 'success'
    elif status==SignatureStatusEnum.PAID:
        color= 'success'
    return color


class ProjectManagerParameterEnum(TextChoices):
    SHOW_FAVORITE_OPEN_ON_HOME="نمایش لیست مورد علاقه به صورت گسترده در خانه",_("نمایش لیست مورد علاقه به صورت گسترده در خانه")
class DeviceConfiguratinoEnum(TextChoices):
    MAC_ADDRESS="MAC Address",_("MAC Address")
    LOCATION="location",_("location")
    TYPE="type",_("type")
    IP="ip",_("ip")
    USERNAME="username",_("username")
    PASSWORD="password",_("password")
    VERSION="version",_("version")
    SERIAL_NO="serial no",_("serial no")