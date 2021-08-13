from django.utils.translation import gettext as _

from django.db.models import TextChoices

class GameScenarioEnum(TextChoices):
    TOFANG_DAR='TOFANG_DAR',_('TOFANG_DAR')
    GROGAN_GIR='GROGAN_GIR',_('GROGAN_GIR')
    RUH='RUH',_('RUH')

class GameRoleEnum(TextChoices):
    GOD_FATHER='GOD_FATHER',_('GOD_FATHER')
    MAFIA='MAFIA',_('MAFIA')
    SHARVAND='SHARVAND',_('SHARVAND')
    GUARD='GUARD',_('GUARD')
    SNIPPER='SNIPPER',_('SNIPPER')
    COWBOY='COWBOY',_('COWBOY')
    TERRORIST='TERRORIST',_('TERRORIST')
    DOCTOR='DOCTOR',_('DOCTOR')
    DETECTIVE='DETECTIVE',_('DETECTIVE')