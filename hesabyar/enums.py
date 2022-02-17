from django.utils.translation import gettext as _
from django.db.models import TextChoices
class GuaranteeTypeEnum(TextChoices):
    REPAIR="تعمیر",_("تعمیر")
    CHANGE="تعویض",_("تعویض")
class GuaranteeStatusEnum(TextChoices):
    VALID="معتبر",_("معتبر")
    INVALID="نامعتبر",_("نامعتبر")
    OVERED="پایان یافته",_("پایان یافته")
    IN_PROGRESS="در جریان",_("در جریان")
    CHANGED="تعویض شده",_("تعویض شده")
    REPAIRED="تعمیر شده",_("تعمیر شده")
    DENIED="برگشت داده شده",_("برگشت داده شده")
class WareHouseSheetDirectionEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار")
class WareHouseSheetStatusEnum(TextChoices):
    INITIAL="تعریف اولیه",_("تعریف اولیه")
    IN_PROGRESS="در جریان",_("در جریان")
    DONE="تمام شده",_("تمام شده") 
class ChequeStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    RETURNED="برگشت خورده",_("برگشت خورده")
    PASSED="پاس شده",_("پاس شده")
    PAID="تسویه شده",_("تسویه شده")
class InvoicePaymentMethodEnum(TextChoices):
    NO_PAYMENT="پرداخت نشده",_("پرداخت نشده")
    CHEQUE="چک",_("چک")
    POS="کارتخوان",_("کارتخوان")
    CARD="کارت به کارت",_("کارت به کارت")
    IN_CASH="پرداخت نقدی",_("پرداخت نقدی")

class SpendTypeEnum(TextChoices):
    COST="هزینه",("هزینه")
    WAGE="حقوق",("حقوق")
class CostTypeEnum(TextChoices):
    WATER="هزینه آب",_("هزینه آب")
    TELEPHONE="هزینه تلفن",_("هزینه تلفن")
    ELECTRICITY="هزینه برق",_("هزینه برق")
    INTERNET="هزینه اینترنت",_("هزینه اینترنت")
    GAS="هزینه گاز",_("هزینه گاز")
    TRANSPORT="هزینه حمل ونقل",_("هزینه حمل ونقل")
    RENT="هزینه اجاره",_("هزینه اجاره")
class PaymentMethodEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    MOBILE_BANK="همراه بانک",_("همراه بانک")
    IN_CASH="نقدی",_("نقدی")
    CHEQUE="چک",_("چک")
    POS="کارتخوان",_("کارتخوان")
    CARD="کارت به کارت",_("کارت به کارت")
class TransactionStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    IN_PROGRESS="در جریان",_("در جریان")
    DELIVERED="تحویل شده",_("تحویل شده")
    APPROVED="تایید شده",_("تایید شده")
    CANCELED="کنسل شده",_("کنسل شده")
    PASSED="پاس شده",_("پاس شده")
