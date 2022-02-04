from django import forms

class AddFinancialDocumentForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)
    document_datetime=forms.CharField(max_length=20, required=True)
    bestankar=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=True)
    bedehkar=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=True)