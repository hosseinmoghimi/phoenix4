from django import forms

class AddPageForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=True)
    
