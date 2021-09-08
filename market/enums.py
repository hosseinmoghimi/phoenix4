from django.utils.translation import gettext as _
from django.db.models import TextChoices

class OrderStatusEnum(TextChoices):
    CHECKED_OUT="تسویه شده",_("تسویه شده")
    PACKING="در حال بسته بندی",_("در حال بسته بندی")
    SHIPPED="حمل شده",_("حمل شده")
    PACKED="بسته بندی شده",_("بسته بندی شده")
    DELIVERED="تحویل شده",_("تحویل شده")

class ParameterEnum(TextChoices):
    SHOP_HEADER_TITLE='عنوان فروشگاه'
    SHOP_HEADER_SLOGAN='شعار فروشگاه'
    SHOP_HEADER_IMAGE='تصویر بنر فروشگاه'

class ShopLevelEnum(TextChoices):
    REGULAR='مشتری عادی'
    CO_WORKER='همکار'
    WHOLE_SALE='توزیع کننده عمده'
    RETAIL='توزیع کننده خرد'