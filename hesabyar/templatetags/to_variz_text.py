from django import template
register = template.Library()
@register.filter
def to_variz_text(bank_account):
    text=" جهت واریز : "
    if bank_account.account_no:
        text+=" شماره حساب : "+bank_account.account_no
    if bank_account.card_no:
        text+=" شماره کارت : "+bank_account.card_no
    if bank_account.shaba_no:
        text+=" شماره شبا : "+bank_account.shaba_no
    if bank_account.profile:
        text+=" به نام  : "+bank_account.profile.name
    return text