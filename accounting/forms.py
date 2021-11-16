from django import forms
class AddTransactionForm(forms.Form):
    title=forms.CharField(max_length=2000,required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    date_paid=forms.CharField(max_length=20,required=False)
    description=forms.CharField(max_length=2000,required=False)
    payment_method=forms.CharField(max_length=200,required=False)
    date_paid=forms.CharField(max_length=200,required=False)