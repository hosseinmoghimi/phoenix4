from django.utils.translation import gettext as _
from django.db.models import TextChoices
class WareHouseSheetDirectionEnum(TextChoices):
    ENTER="ورود به انبار",_("ورود به انبار")
    EXIT="خروج از انبار",_("خروج از انبار")
class WareHouseSheetStatusEnum(TextChoices):
    INITIAL="تعریف اولیه",_("تعریف اولیه")
    IN_PROGRESS="در جریان",_("در جریان")
    DONE="تمام شده",_("تمام شده")
class InvoiceStatusEnum(TextChoices):
    DRAFT="پیش فاکتور",_("پیش فاکتور")
    IN_PROGRESS="در جریان",_("در جریان")
    DELIVERED="تحویل شده",_("تحویل شده")