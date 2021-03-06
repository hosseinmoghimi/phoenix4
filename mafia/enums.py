from django.utils.translation import gettext as _

from django.db.models import TextChoices

class NightActEnum(TextChoices):
    HEAL_BY_DOCTOR="نجات پزشک",_("نجات پزشک")

class GameDayNightStatusEnum(TextChoices):
    RUNNING="در حال اجرا",_("در حال اجرا")
    FINISHED="پایان یافته",_("پایان یافته")

class GameRoleStateEnum(TextChoices):
    ALIVE="زنده",_("زنده")
    SHOTTED="شات شده",_("شات شده")
    FIRED="اخراج شده",_("اخراج شده")

class GameStatusEnums(TextChoices):
    CREATING='در حال ساخت',_('در حال ساخت')
    ROLING='در حال نقش دهی',_('در حال نقش دهی')
    INTRODUCING="معارفه",_("معارفه")
    STARTED='در حال اجرا',_('در حال اجرا')
    DAY_IN_PROGRESS="بازی در فاز روز",_("بازی در فاز روز")
    COURT_VOTING="رای گیری برای ورود به دادگاه",_("رای گیری برای ورود به دادگاه")
    ACCUSE_VOTING="رای گیری برای خروج از شهر",_("رای گیری برای خروج از شهر")
    NIGHT_IN_PROGRESS="بازی در فاز شب",_("بازی در فاز شب")
    FINISHED='تمام شده',_('تمام شده')


class GameScenarioEnum(TextChoices):
    TOFANG_DAR='تفنگ دار',_('تفنگ دار')
    GROGAN_GIR='گروگان گیر',_('گروگان گیر')
    MOZAKERE='مذاکره',_('مذاکره')
    DANESH_AMUZ='دانش آموز',_('دانش آموز')
    RUH='روح',_('روح')

class VoteLevelEnum(TextChoices):
    COURT='ورود به دادگاه',_('ورود به دادگاه')
    ACCUSE='خروج از شهر',_('خروج از شهر')


class SideEnums(TextChoices):
    MAFIA='مافیا',_('مافیا')
    CITIZEN='شهروند',_('شهروند')
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