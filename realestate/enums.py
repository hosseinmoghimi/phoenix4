from django.utils.translation import gettext as _
from django.db.models import TextChoices

class FloorEnum(TextChoices):
    UNDER_GROUND='زیر زمین',_('زیر زمین')
    HAMKAF='همکف',_('همکف')
    FIRST='اول',_('اول')
    SECOND='دوم',_('دوم')
    THIRD='سوم',_('سوم')
    FOURTH='چهارم',_('چهارم')
class KitchenTypeEnum(TextChoices):
    REGULAR='معمولی',_('معمولی')
    ISLAND='جزیره',_('جزیره')