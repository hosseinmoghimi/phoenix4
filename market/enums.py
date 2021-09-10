from django.utils.translation import gettext as _
from django.db.models import TextChoices

class OrderStatusEnum(TextChoices):
    CHECKED_OUT="تسویه شده",_("تسویه شده")
    PACKING="در حال بسته بندی",_("در حال بسته بندی")
    SHIPPED="حمل شده",_("حمل شده")
    PACKED="بسته بندی شده",_("بسته بندی شده")
    DELIVERED="تحویل شده",_("تحویل شده")




class OrderStatusEnum(TextChoices):
    PROCESSING = 'درحال پردازش', _('درحال پردازش')
    COMPLETED = 'کامل شده', _('کامل شده')
    CANCELED = 'کنسل شده', _('کنسل شده')
    PENDING = 'درحال انتظار', _('درحال انتظار')
    SHIPPED = 'ارسال شده', _('ارسال شده')
    DELIVERED = 'تحویل شده', _('تحویل شده')
    PACKING = 'درحال بسته بندی', _('درحال بسته بندی')
    ACCEPTED='پذیرفته شده' , _('پذیرفته شده')
    PACKED = 'بسته بندی شده', _('بسته بندی شده')
    ON_HOLD = 'معلق', _('معلق')
    CONFIRMED = 'تایید مشتری', _('تایید مشتری')



class PictureEnum(TextChoices):
    CART_HEADER='تصویر '+'سربرگ سبد خرید'
    ORDER_HEADER='تصویر '+'سربرگ سبد سفارش'
    ORDERS_HEADER='تصویر '+'سربرگ سفارشات'
class ParameterEnum(TextChoices):
    SHOP_HEADER_TITLE='عنوان فروشگاه'
    SHOP_HEADER_SLOGAN='شعار فروشگاه'
    SHOP_HEADER_IMAGE='تصویر بنر فروشگاه'

class ShopLevelEnum(TextChoices):
    REGULAR='مشتری عادی'
    CO_WORKER='همکار'
    WHOLE_SALE='توزیع کننده عمده'
    RETAIL='توزیع کننده خرد'