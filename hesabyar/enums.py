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
class ChequeStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    RETURNED="برگشت خورده",_("برگشت خورده")
    PAID="تسویه شده",_("تسویه شده")
class InvoicePaymentMethodEnum(TextChoices):
    NO_PAYMENT="پرداخت نشده",_("پرداخت نشده")
    CARD="کارتخوان",_("کارتخوان")
    IN_CASH="پرداخت نقدی",_("پرداخت نقدی")