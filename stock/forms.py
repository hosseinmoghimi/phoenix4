from django import forms

class ImportDataForm(forms.Form):
    data=forms.CharField(max_length=1000000,required=True)
class SearchForm(forms.Form):
    app_name=forms.CharField(max_length=50, required=True)
    search_for=forms.CharField(max_length=200,required=True)

class AddDocumentForm(forms.Form):
    stock_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)

class AddPaymentForm(forms.Form):
    amount=forms.IntegerField(required=True)
    share_holder_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)