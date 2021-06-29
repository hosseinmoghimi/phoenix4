from django import forms
class AddTransactionForm(forms.Form):
    pay_to=forms.IntegerField(required=True)
    pay_from=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    date_paid=forms.CharField(max_length=20,required=False)