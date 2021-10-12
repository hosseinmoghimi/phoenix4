import django
from .apps import APP_NAME
from django.db.models import TextChoices
from django.utils.translation import gettext as _
class SalaryTitleEnum(TextChoices):
    BASE_SALARY='حقوق پایه',_('حقوق پایه')
    CHILDREN='حق فرزند',_('حق فرزند')
    WIFE='حق همسر',_('حق همسر')
    WEATHER='بدی آب و هوا',_('بدی آب و هوا')
    TAX='مالیات',_('مالیات')
class SalaryDirectionEnum(TextChoices):
    MAZAYA='مزایا',_('مزایا')
    KOSURAT='کسورات',_('کسورات')

