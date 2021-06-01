from core.enums import *
from django.utils.translation import gettext as _
class MaterialUnitNameEnum(TextChoices):
    ADAD="عدد",_("عدد")
    GERAM="گرم",_("گرم")
    KILOGERAM="کیلوگرم",_("کیلوگرم")
    TON="تن",_("تن")
    METER="متر",_("متر")

class SignatureStatusEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال بررسی',_('درحال بررسی')
    DENIED='رد شده',_('ردشده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    PURCHASING='درحال خرید',_('درحال خرید')

class MaterialRequestStatusEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    INITIAL='تعریف اولیه در سیستم',_('تعریف اولیه در سیستم')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال بررسی',_('در حال بررسی')
    DENIED='رد شده',_('رد شده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    PURCHASING='در حال خرید',_('در حال خرید')
    ALREADY_AVAILABLE='متعلق به کارفرما',_('متعلق به کارفرما')



class AssignmentStatusEnum(TextChoices):
    DEFAULT='تعریف اولیه',_('تعریف اولیه')
    IN_PROGRESS='در جریان',_('در جریان')
    DONE='انجام شده',_('انجام شده')
    STOPEED='متوقف شده',_('متوقف شده')
    DENIED='رد شده',_('رد شده')
    INITIAL='ابلاغ شده',_('ابلاغ شده')
        

def StatusColor(status):
    color="primary"
    if status==AssignmentStatusEnum.DEFAULT:
        color= 'rose'
    elif status==AssignmentStatusEnum.IN_PROGRESS:
        color= 'info'
    elif status==AssignmentStatusEnum.DONE:
        color= 'success'
    elif status==AssignmentStatusEnum.STOPEED:
        color= 'secondary'
    elif status==AssignmentStatusEnum.DENIED:
        color= 'danger'
    elif status==MaterialRequestStatusEnum.DEFAULT:
        color= 'rose'
    elif status==MaterialRequestStatusEnum.ALREADY_AVAILABLE:
        color= 'info'
    elif status==MaterialRequestStatusEnum.IN_PROGRESS:
        color= 'info'
    elif status==MaterialRequestStatusEnum.ACCEPTED:
        color= 'success'
    elif status==MaterialRequestStatusEnum.DELIVERED:
        color= 'success'
    elif status==MaterialRequestStatusEnum.DENIED:
        color= 'danger'
    elif status==MaterialRequestStatusEnum.PURCHASING:
        color= 'primary'
    return color