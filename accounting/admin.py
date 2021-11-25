from accounting.models import Asset, AssetTransaction, BankAccount, FinancialAccount, MarketOrderTransaction, MoneyTransaction, ProjectTransaction, Transaction
from django.contrib import admin

admin.site.register(BankAccount)
admin.site.register(FinancialAccount)
admin.site.register(MoneyTransaction)
admin.site.register(Asset)
admin.site.register(AssetTransaction)
admin.site.register(MarketOrderTransaction)
admin.site.register(ProjectTransaction)