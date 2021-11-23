from core import enums as CoreEnums
from django.utils.translation import gettext as _
from django.db.models import TextChoices
class ParameterEnums(TextChoices):
    LOG_PER_PAGE='لاگ در هر صفحه',_('لاگ در هر صفحه')
class RelayStateEnum(TextChoices):
    ALWAYS_ON='ALWAYS_ON',_('ALWAYS_ON')
    ALWAYS_OFF='ALWAYS_OFF',_('ALWAYS_OFF')
    ON_THEN_OFF='ON_THEN_OFF',_('ON_THEN_OFF')
    OFF_THEN_ON='OFF_THEN_ON',_('OFF_THEN_ON')
    ON_OFF_ON_OFF='ON_OFF_ON_OFF',_('ON_OFF_ON_OFF')
    OFF_ON_OFF_ON='OFF_ON_OFF_ON',_('OFF_ON_OFF_ON')

