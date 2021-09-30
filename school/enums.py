from django.db.models.enums import TextChoices
from .apps import APP_NAME
from django.utils.translation import gettext as _
class AttendanceStatusEnum(TextChoices):
    PRESENT="حضور",_("حضور")
    ABSENT="غیبت",_("غیبت")
    DELAY="حضور با تاخیر",_("حضور با تاخیر")
