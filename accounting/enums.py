from django.db.models import TextChoices
from django.utils.translation import gettext as _
class BankNameEnum(TextChoices):
    MELLI='بانک ملی',_('بانک ملی')
    MELLAT='بانک ملت',_('بانک ملت')
    SEPAH='بانک سپه',_('بانک سپه')
    REFAH='بانک رفاه',_('بانک رفاه')
    MASKAN='بانک مسکن',_('بانک مسکن')
    TAAVON='بانک توسعه تعاون',_('بانک توسعه تعاون')
    
