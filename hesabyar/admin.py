from django.contrib import admin

from .models import Guarantee,Bank, BankAccount, Cheque, FinancialAccount, FinancialDocument, FinancialDocumentCategory, FinancialYear, Guarantee, Invoice,Payment, InvoiceLine, Product, ProductOrService, Service, Store, Tag, WareHouse, WareHouseSheet

# Register your models here.
admin.site.register(WareHouse)
admin.site.register(Guarantee)
admin.site.register(WareHouseSheet)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Service)
admin.site.register(InvoiceLine)
admin.site.register(FinancialAccount)
# admin.site.register(ProfileFinancialAccount)
admin.site.register(FinancialYear)
admin.site.register(FinancialDocument)
admin.site.register(Tag)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Store)
admin.site.register(Cheque)
admin.site.register(FinancialDocumentCategory)