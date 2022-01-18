from core.enums import *
from django.utils.translation import gettext as _

class LetterStatusEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    DELIVERED='تحویل شده',_('تحویل شده')
    IN_PROGRESS='در حال بررسی',_('درحال بررسی')

    
def StatusColor(status):
    color="primary"
    if status==LetterStatusEnum.INITIAL:
        color= 'primary'
    return color