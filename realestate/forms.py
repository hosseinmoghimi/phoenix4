from django import forms

class AddPropertyLocationForm(forms.Form):
    property_id=forms.IntegerField(required=True)
    location=forms.CharField(max_length=5000, required=True)