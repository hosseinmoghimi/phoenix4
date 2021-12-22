from django.utils.translation import gettext as _
from django.db.models import TextChoices

class OrderStatusEnum(TextChoices):
    CHECKED_OUT="تسویه شده",_("تسویه شده")
    PACKING="در حال بسته بندی",_("در حال بسته بندی")
    SHIPPED="حمل شده",_("حمل شده")
    PACKED="بسته بندی شده",_("بسته بندی شده")
    DELIVERED="تحویل شده",_("تحویل شده")




class DegreeLevelEnum(TextChoices):
    DIPLOM = 'دیپلم', _('دیپلم')
    KARDANI = 'کاردانی', _('کاردانی')
    KARSHENASI = 'کارشناسی', _('کارشناسی')
    KARSHENASI_ARSHAD = 'کارشناسی ارشد', _('کارشناسی ارشد')
    PHD = 'دکتری', _('دکتری')


class EmployeeEnum(TextChoices):
    CEO='سرپرست',_('سرپرست')  
    GUARD='نگهبان',_('نگهبان')      
    MANAGER='مدیر',_('مدیر')      
    TECHNICAL='فنی',_('فنی')    
    DEFAULT='تایید نشده',_('تایید نشده')
    ACCOUNTANT='حسابدار',_('حسابدار')
    CASHIER='صندوقدار',_('صندوقدار')
    

class OrderStatusEnum(TextChoices):
    CART="سبد خرید",_("سبد خرید")
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


class OrderLineStatusEnum(TextChoices):
    CART="سبد خرید",_("سبد خرید")
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
    ORDER_LINE_HEADER="تصویر سربرگ ریز سفارش",_("تصویر سربرگ ریز سفارش")
    CUSTOMER_HEADER='تصویر سربرگ صفحه مشتری',_('تصویر سربرگ صفحه مشتری')
    BRANDS_IMAGE_HEADER='تصویر سربرگ صفحه برند ها',_('تصویر سربرگ صفحه برند ها')
    CART_HEADER='تصویر سربرگ سبد خرید',_('تصویر سربرگ سبد خرید')
    SEARCH_HEADER='تصویر سربرگ صفحه جستجو',_('تصویر سربرگ صفحه جستجو')
    ORDER_HEADER='تصویر سربرگ سبد سفارش' ,_('تصویر سربرگ سبد سفارش')
    ORDERS_HEADER='تصویر سربرگ سفارشات',_('تصویر سربرگ سفارشات')
    GUARANTEE_HEADER="تصویر سربرگ گارانتی",_("تصویر سربرگ گارانتی")
class ParameterEnum(TextChoices):
    BRANDS_SLOGAN="شعار صفحه برند ها",_("شعار صفحه برند ها")
    SHOP_HEADER_TITLE='عنوان صفحه خانه برای فروشگاه',_('عنوان صفحه خانه برای فروشگاه')
    SHOP_HEADER_LINK='لینک فروشگاه',_('لینک فروشگاه')
    SHOP_HEADER_SLOGAN='شعار فروشگاه',_('شعار فروشگاه')
    SHOP_HEADER_IMAGE='تصویر بنر فروشگاه',_('تصویر بنر فروشگاه')

class ShopLevelEnum(TextChoices):
    REGULAR='مشتری عادی',_('مشتری عادی')
    CO_WORKER='همکار',_('همکار')
    WHOLE_SALE='توزیع کننده عمده',_('توزیع کننده عمده')
    RETAIL='توزیع کننده خرد',_('توزیع کننده خرد')