from django import forms

class ImportDataForm(forms.Form):
    data=forms.CharField(max_length=1000000,required=True)
class SearchForm(forms.Form):
    app_name=forms.CharField(max_length=50, required=True)
    search_for=forms.CharField(max_length=200,required=True)

class AddStockForm(forms.Form):
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50,required=True)
    stock1=forms.IntegerField(required=True)
    stock2=forms.IntegerField(required=True)
    agent_id=forms.IntegerField(required=True)
class AddDocumentForm(forms.Form):
    stock_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)

class AddPaymentForm(forms.Form):
    stock_id=forms.IntegerField(required=True)
    value=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)
    date_paid=forms.CharField(max_length=50,required=True)
    payment_type=forms.CharField(max_length=50, required=True)