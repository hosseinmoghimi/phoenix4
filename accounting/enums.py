from django.db.models import TextChoices
from django.utils.translation import gettext as _
class BankNameEnum(TextChoices):
    MELLI='بانک ملی',_('بانک ملی')
    MELLAT='بانک ملت',_('بانک ملت')
    SEPAH='بانک سپه',_('بانک سپه')
    REFAH='بانک رفاه',_('بانک رفاه')
    MASKAN='بانک مسکن',_('بانک مسکن')
    TAAVON='بانک توسعه تعاون',_('بانک توسعه تعاون')
    
class PaymetMethodEnum(TextChoices):
    CASH="وجه نقد",_("وجه نقد")
    CARD="کارت به کارت",_("کارت به کارت")
    BANK="واریزی بانک",_("واریزی بانک")
    CHEQUE="چک",_("چک")