from accounting.models import BankAccount, FinancialAccount, Transaction
from django.contrib import admin

admin.site.register(BankAccount)
admin.site.register(FinancialAccount)
admin.site.register(Transaction)