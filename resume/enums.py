from django.db.models import TextChoices
from django.utils.translation import gettext as _
class ResumeItemEnum(TextChoices):
    FACT='FACT'
    SKILL='SKILL'
class IconEnum(TextChoices):
    smile='<i class="bi bi-emoji-smile"></i>',_('<i class="bi bi-emoji-smile"></i>')
    richtext='<i class="bi bi-journal-richtext"></i>',_('<i class="bi bi-journal-richtext"></i>')
    headset='<i class="bi bi-headset"></i>',_('<i class="bi bi-headset"></i>')
    award='<i class="bi bi-award"></i>',_('<i class="bi bi-award"></i>')
class FilterEnum(TextChoices):
    app='app',_('app')
    card='card',_('card')
    web='web',_('web')
class ServiceColorEnum(TextChoices):
    blue='blue',_('blue')
    orange='orange',_('orange')
    pink='pink',_('pink')
    yellow='yellow',_('yellow')
    red='red',_('red')
    teal='teal',_('teal')
class LanguageEnum(TextChoices):
    ENGLISH='english',_('english')
    DUTCH='dutch',_('dutch')
    FARSI='farsi',_('farsi')
    RUSSIAN='russian',_('russian')
    ARABIC='arabic',_('arabic')
def languageToIndex(*args, **kwargs):
    if 'language' in kwargs:
        if kwargs['language']==LanguageEnum.FARSI:
            return 2
        if kwargs['language']==LanguageEnum.ENGLISH:
            return 1
        return 1
        
    if 'index' in kwargs:
        if kwargs['index']==2:
            return LanguageEnum.FARSI
        if kwargs['index']==1:
            return LanguageEnum.ENGLISH
        return LanguageEnum.ENGLISH
    
        
    

class LinkClassEnum(TextChoices):
    twitter="""twitter"""
    facebook="""facebook"""
    instagram="""instagram"""
    google_plus="""skype"""
    linkedin="""linkedin"""

class IconEnum(TextChoices):
    twitter="""<i class="bx bxl-twitter"></i>"""
    facebook="""<i class="bx bxl-facebook"></i>"""
    instagram="""<i class="bx bxl-instagram"></i>"""
    google_plus="""<i class="bx bxl-skype"></i>"""
    linkedin="""<i class="bx bxl-linkedin"></i>"""
    journal="""<i class="bi bi-journal-richtext"></i>"""
    emoji="""<i class="bi bi-emoji-smile"></i>"""
    headset="""<i class="bi bi-headset"></i>"""
    award="""<i class="bi bi-award"></i>"""