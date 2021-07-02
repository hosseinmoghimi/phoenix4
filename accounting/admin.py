from accounting.models import Asset, BankAccount, FinancialAccount, Transaction
from django.contrib import admin

admin.site.register(BankAccount)
admin.site.register(FinancialAccount)
admin.site.register(Transaction)
admin.site.register(Asset)