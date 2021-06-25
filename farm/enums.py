from core import enums as CoreEnums
from django.utils.translation import gettext as _
class AnimalCategoryEnum(CoreEnums.TextChoices):
    COW='گاو',_("گاو")
    CHICKEN='مرغ',_("مرغ")
    SHEEP='گوسفند',_("گوسفند")
    OSTRICH='شترمرغ',_("شترمرغ")
    TURKEY='بوقلمون',_("بوقلمون")