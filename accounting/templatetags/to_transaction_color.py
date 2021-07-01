from django import template
register = template.Library()

@register.filter
def to_transaction_color(value):
    color="primary"
    try:
        value=int(value)
        if value>0:
            color="success"
        if value<0:
            color="danger"
    except:
        pass
    return color
    

