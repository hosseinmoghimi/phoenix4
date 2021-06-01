from django.contrib import admin
from .models import BasicPage, Icon, Image, Parameter, Tag,Link,PageDocument,PageLink,Document

admin.site.register(Parameter)
admin.site.register(BasicPage)
admin.site.register(Icon)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Document)
admin.site.register(PageLink)
admin.site.register(PageDocument)