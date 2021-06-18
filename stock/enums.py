from django.db.models import TextChoices
from core import enums as CoreEnums
from django.utils.translation import gettext as _
class ParametersEnum(TextChoices):
    STOCK1="STOCK1",_("STOCK1")
    STOCK2="STOCK2",_("STOCK2")