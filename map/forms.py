from django import forms

class AddLocationForm(forms.Form):
    page_id=forms.IntegerField(required=False)
    location=forms.CharField(max_length=500,required=True)
    title=forms.CharField(max_length=500,required=False)
               