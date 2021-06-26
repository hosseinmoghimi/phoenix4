from django.db.models import TextChoices
from django.utils.translation import gettext as _
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