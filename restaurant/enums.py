from django.db.models import TextChoices
from django.utils.translation import TranslatorCommentWarning, gettext as _

class MealTypeEnum(TextChoices):
    BREAK_FAST="صبحانه",_("صبحانه")
    LUNCH="ناهار",_("ناهار")
    DINNER="شام",_("شام")