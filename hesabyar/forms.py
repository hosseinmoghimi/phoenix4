from django import forms

class SearchFrom(forms.Form):
    search_for=forms.CharField( max_length=200, required=True)
class AddFinancialDocumentForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)
    document_datetime=forms.CharField(max_length=20, required=True)
    bestankar=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=True)
    bedehkar=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=True)
class SearchForm(forms.Form):
    search_for=forms.CharField( max_length=500, required=True)

class AddChequeForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
class AddPaymentForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    transaction_datetime=forms.CharField( max_length=50, required=True)
    payment_method=forms.CharField( max_length=50, required=True)
    description=forms.CharField( max_length=50, required=False)
class EditInvoiceForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    discount=forms.IntegerField(required=True)
    lines=forms.CharField(max_length=50000, required=True)
    description=forms.CharField(max_length=5000, required=False)
    invoice_datetime=forms.CharField(max_length=20, required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    tax_percent=forms.IntegerField(required=True)
    ship_fee=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
    payment_method=forms.CharField(max_length=50, required=True)
    