from django.db.models.enums import TextChoices
from .apps import APP_NAME
from django.utils.translation import gettext as _
class AttendanceStatusEnum(TextChoices):
    PRESENT="حاضر",_("حاضر")
    ABSENT="غایب",_("غایب")
    NOT_SET="نا مشخص",_("نا مشخص")
    DELAY="تاخیر",_("تاخیر")
    TASHVIGH="تشویق",_("تشویق")
    TANBIH="تنبیه",_("تنبیه")
