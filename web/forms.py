from django import forms
from django.db.models.fields import BooleanField
from django.http import request
from .apps import APP_NAME  
class AddContactMessageForm(forms.Form):
    subject=forms.CharField(max_length=200, required=True)
    email=forms.CharField(max_length=50, required=True)
    mobile=forms.CharField(max_length=13, required=False)
    message=forms.CharField(max_length=500, required=True)
    full_name=forms.CharField(max_length=50, required=True)
    app_name=forms.CharField(max_length=50, required=True)

class AddPageForm(forms.Form):
    title=forms.CharField(max_length=200, required=True)
    for_home=forms.BooleanField(required=False)
    
    
class SearchForm(forms.Form):
    url=("/"+APP_NAME+"/search/")
    search_for=forms.CharField(max_length=200, required=True)
    
    