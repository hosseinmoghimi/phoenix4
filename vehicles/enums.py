from core import enums as CoreEnums
from django.db.models import TextChoices
from django.utils.translation import gettext as _
class MaintenanceEnum(TextChoices):
    WASH="شستشو",_("شستشو")
    NEW_WATER='آب رادیات جدید',_('آب رادیات جدید')
    NEW_FUEL='سوخت جدید',_('سوخت جدید')
    REPAIR_ENGINE='تعمیر موتور',_('تعمیر موتور')
    REPAIR_GEARBOX='تعمیر گیربکس',_('تعمیر گیربکس')
    NEW_INSURANCE='بیمه جدید',_('بیمه جدید')
    NEW_TIRE='لاستیک جدید',_('لاستیک جدید')
    NEW_CHAIN='زنجیر جدید',_('زنجیر جدید')
    NEW_GLASS='شیشه جدید',_('شیشه جدید')
    NEW_OIL='تعویض روغن',_('تعویض روغن')
    NEW_AIR_FILTER='فیلتر هوای جدید',_('فیلتر هوای جدید')
    NEW_OIL_FILTER='فیلتر روغن جدید',_('فیلتر روغن جدید')
class WorkEventEnum(TextChoices):
    FLAT_TIRE='لاستیک پنچر',_('لاستیک پنچر')
    BROKEN_GLASS="شیشه شکسته",_("شیشه شکسته")
    CRASH1="خسارت مالی",_("خسارت مالی")
    CRASH2="خسارت جانی",_("خسارت جانی")
    # aaaa=aaaa,_("aaaa")
    # aaaa=aaaa,_("aaaa")
class VehicleBrandEnum(TextChoices):
    TOYOTA='تویوتا',_('تویوتا')
    BENZ='بنز',_('بنز')
    ISUZU='ایسوزو',_('ایسوزو')
    SCANIA='اسکانیا',_('اسکانیا')
    VOLVO='ولوو',_('ولوو')
    CATERPILAR='کاترپیلار',_('کاترپیلار')
    HYUNDAI='هیوندای',_('هیوندای')
    HOWO='هووو',_('هووو')
    DONG_FENG='دانگ فنگ',_('دانگ فنگ')
    SAIPA='سایپا',_('سایپا')
    IRAN_KHODRO='ایران خودرو',_('ایران خودرو')
    XCMG='XCMG',_('XCMG')
    

class VehicleColorEnum(TextChoices):
    SEFID='سفید',_('سفید')
    SIAH='سیاه',_('سیاه')
    NOK_MEDADI='نوک مدادی',_('نوک مدادی')
    DOLPHINI='دلفینی',_('دلفینی')
    BEZH='بژ',_('بژ')
    GHERMEZ='قرمز',_('قرمز')

class VehicleTypeEnum(TextChoices):
    TRUCK='وانت',_('وانت')
    SEDAN='سواری',_('سواری')
    BUS='اتوبوس',_('اتوبوس')
    TAXI='تاکسی',_('تاکسی')
    GRADER='گریدر',_('گریدر')
    LOADER='لودر',_('لودر')
    TRAILER='تریلی',_('تریلی')
    CONTAINER='کانتینر',_('کانتینر')
    SEPERATOR='سپراتور',_('سپراتور')
    TRUCK2='خاور',_('خاور')