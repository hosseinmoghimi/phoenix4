from core.constants import CURRENCY
from core.errors import LEO_ERRORS
from django import template
register = template.Library()

@register.filter
def to_million_price(value):
    milliards=0
    millions=value
    if value>1000:
        milliards=int(value/1000)
        millions=value-1000*milliards
    if milliards==0 and millions==0:
        return None
    if milliards==0 and millions>0:
        return str(millions)+" " + "میلیون "+CURRENCY
    if millions==0 and milliards>0:
        return str(milliards)+" " + "میلیارد "+CURRENCY
    if milliards>0 and millions>0:
        return str(milliards)+ " میلیارد و "+str(millions)+ " میلیون "+CURRENCY
    
     


