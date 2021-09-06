from django.db.models.enums import TextChoices
from django.utils.translation import gettext as _

class ParameterEnum(TextChoices):
    FeatureTitle="عنوان خدمات ما",_("عنوان خدمات ما")
    FeatureDescription="توضیح خدمات ما",_("توضیح خدمات ما")
    BlogsTitle="عنوان مقالات",_("عنوان مقالات")
    BlogsDescription="توضیح مقالات",_("توضیح مقالات")
    OurWorksPreTitle="پیش عنوان پروژه های ما",_("پیش عنوان پروژه های ما")
    OurWorksTitle="عنوان پروژه های ما",_("عنوان پروژه های ما")
    OurWorksDescription="توضیح پروژه های ما",_("توضیح پروژه های ما")
    OurTeamTitle="عنوان تیم ما",_("عنوان تیم ما")
    OurTeamDescription="توضیح تیم ما",_("توضیح تیم ما")

