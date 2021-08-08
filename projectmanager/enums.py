from core.enums import *
from django.utils.translation import gettext as _



class SignatureStatusEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال بررسی',_('درحال بررسی')
    DENIED='رد شده',_('ردشده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    PURCHASING='درحال خرید',_('درحال خرید')
    REQUESTED='درخواست شده',_('درخواست شده')


class ProjectStatusEnum(TextChoices):
    INITIAL='تعریف اولیه',_('تعریف اولیه')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال اجرا',_('درحال اجرا')
    DENIED='رد شده',_('ردشده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    REQUESTED='درخواست شده',_('درخواست شده')
    CANCELED='کنسل شده',_('کنسل شده')

class RequestStatusEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    INITIAL='تعریف اولیه در سیستم',_('تعریف اولیه در سیستم')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال بررسی',_('در حال بررسی')
    DENIED='رد شده',_('رد شده')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    REQUESTED='درخواست شده',_('درخواست شده')
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
    if status==ProjectStatusEnum.INITIAL:
        color= 'primary'
    elif status==ProjectStatusEnum.IN_PROGRESS:
        color= 'warning'
    elif status==ProjectStatusEnum.DENIED:
        color= 'danger'
    elif status==ProjectStatusEnum.DELIVERED:
        color= 'dark'
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
    elif status==RequestStatusEnum.ALREADY_AVAILABLE:
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
        color= 'primary'
    return color