from django.contrib import admin

from hesabyar.models import Bank, BankAccount, Cash, EmployerFinancialAccount, FinancialDocument, FinancialYear, ProfileFinancialAccount

# Register your models here.
admin.site.register(ProfileFinancialAccount)
admin.site.register(FinancialYear)
admin.site.register(FinancialDocument)
admin.site.register(EmployerFinancialAccount)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Cash)