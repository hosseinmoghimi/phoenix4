from django import forms

class AddCryptoTokenForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)