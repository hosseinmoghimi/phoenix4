from .models import PropertyFeature, PropertyMedia,Property,Car
from django.contrib import admin

# Register your models here.
admin.site.register(PropertyMedia)
admin.site.register(Property)
admin.site.register(PropertyFeature)
admin.site.register(Car)