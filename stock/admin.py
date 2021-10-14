from stock.models import Agent, Document, Payment, Stock
from django.contrib import admin

# Register your models here.
admin.site.register(Stock)
admin.site.register(Document)
admin.site.register(Payment)
admin.site.register(Agent)