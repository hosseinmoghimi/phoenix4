from django.contrib import admin
from .models import BasicPage, Icon, Image, Parameter, Tag

admin.site.register(Parameter)
admin.site.register(BasicPage)
admin.site.register(Icon)
admin.site.register(Image)
admin.site.register(Tag)