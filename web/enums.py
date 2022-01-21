from django.db.models.enums import TextChoices
from django.utils.translation import gettext as _

class ParameterEnum(TextChoices):
    OFFICE_ADDRESS="آدرس دفتر",_("آدرس دفتر")
    OFFICE_TEL="تلفن دفتر",_("تلفن دفتر")
    OFFICE_MOBILE="تماس  دفتر",_("تماس  دفتر")
    OFFICE_EMAIL="ایمیل دفتر",_("ایمیل دفتر")
    FeatureTitle="عنوان خدمات ما",_("عنوان خدمات ما")
    FeatureDescription="توضیح خدمات ما",_("توضیح خدمات ما")
    BlogsTitle="عنوان مقالات",_("عنوان مقالات")
    APP_Title="عنوان وب سایت",_("عنوان وب سایت")
    APP_HOME_URL="آدرس خانه وب سایت",_("آدرس خانه وب سایت")
    BlogsDescription="توضیح مقالات",_("توضیح مقالات")
    OurWorksPreTitle="پیش عنوان پروژه های ما",_("پیش عنوان پروژه های ما")
    OurWorksTitle="عنوان پروژه های ما",_("عنوان پروژه های ما")
    OurWorksDescription="توضیح پروژه های ما",_("توضیح پروژه های ما")
    OurTeamTitle="عنوان تیم ما",_("عنوان تیم ما")
    OurTeamDescription="توضیح تیم ما",_("توضیح تیم ما")

