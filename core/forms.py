from django import forms

class AddPageForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=True)
    

class AddPageLinkForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    url=forms.CharField(max_length=100, required=True)
    

class AddPageDocumentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)
    
