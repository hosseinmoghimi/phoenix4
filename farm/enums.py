from core import enums as CoreEnums
from django.utils.translation import gettext as _
class AnimalCategoryEnum(CoreEnums.TextChoices):
    COW='گاو',_("گاو")
    CHICKEN='مرغ',_("مرغ")
    SHEEP='گوسفند',_("گوسفند")
    OSTRICH='شترمرغ',_("شترمرغ")
    TURKEY='بوقلمون',_("بوقلمون")
class CostCategoryEnum(CoreEnums.TextChoices):
    DEFAULT='هزینه',_("هزینه")
    AB='آب',_("آب")
    BARGH='برق',_("برق")
    GAZ='گاز',_("گاز")
    TELEPHONE='تلفن',_("تلفن")
    RENT='اجاره',_("اجاره")
    GUARD="نگهبان",_("نگهبان")
    BUILDING="ساختمانی",_("ساختمانی")