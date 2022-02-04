from django.contrib import admin

from .models import Bank, BankAccount, Cash, FinancialAccount, FinancialDocument, FinancialDocumentCategory, FinancialYear, ProfileFinancialAccount, Store, Tag

# Register your models here.
admin.site.register(FinancialAccount)
admin.site.register(ProfileFinancialAccount)
admin.site.register(FinancialYear)
admin.site.register(FinancialDocument)
admin.site.register(Tag)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Cash)
admin.site.register(Store)
admin.site.register(FinancialDocumentCategory)