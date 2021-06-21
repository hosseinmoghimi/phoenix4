from realestate.models import PropertyFeature, PropertyMedia,Property
from django.contrib import admin

# Register your models here.
admin.site.register(PropertyMedia)
admin.site.register(Property)
admin.site.register(PropertyFeature)