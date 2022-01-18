from django import forms

class AddPropertyLocationForm(forms.Form):
    property_id=forms.IntegerField(required=True)
    location=forms.CharField(max_length=5000, required=True)
    
class AddPropertyFeatureForm(forms.Form):
    property_id=forms.IntegerField(required=True)
    name=forms.CharField(max_length=50, required=True)
    value=forms.CharField(max_length=50, required=True)
class AddPropertyImageForm(forms.Form):
    property_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=50, required=True)