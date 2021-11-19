from django import forms

class AddFoodForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)